import os
import json
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from groq import Groq
import uvicorn
from pyngrok import ngrok
import nest_asyncio

# Load trained model
model = load_model('chatbot_model34.keras')


with open('tokenizer.json') as f:
    tokenizer_data = json.load(f)
tokenizer = tokenizer_from_json(tokenizer_data)


with open('label_encoder.json') as f:
    label_classes = json.load(f)
le = LabelEncoder()
le.classes_ = np.array(label_classes)


with open('extracted/intents.json') as file:
    data = json.load(file)

max_len = model.input_shape[1]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client['chatbot']
prompts_collection = db['prompts']
admin_collection = db['admins']

class ChatRequest(BaseModel):
    message: str

class AdminCredentials(BaseModel):
    username: str
    password: str

admin_sessions = {}

# Groq API setup
os.environ["GROQ_API_KEY"] = "your-api-key"

def groq_response(user_input):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY is not set."

    client = Groq(api_key=api_key)
    system_prompt = {
        "role": "assistant",
        "content": (
            "You are a helpful assistant for IEM Kolkata. "
            "You can assist with queries related to admissions, courses, faculty, campus facilities, and other college-related information. "
            "For any question outside of these topics, reply with: 'Sorry, we are unable to give you the answer at this moment.' "
            "Do not provide unasked data or go off-topic. Stick to college-related queries only. "
            "Always format your response in HTML for a website. Use <strong> for bold text, <ul> and <li> for lists, and <br> for line breaks."
        )
    }

    chat_history = [system_prompt, {"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=450,
        temperature=1.2
    )

    #  response is in HTML format
    response_text = response.choices[0].message.content
    if not any(tag in response_text for tag in ['<strong>', '<ul>', '<li>', '<br>']):
        response_text = convert_to_html(response_text)

    return response_text

def predict_intent(user_input):
    encoded_input = tokenizer.texts_to_sequences([user_input])
    padded_input = pad_sequences(encoded_input, maxlen=max_len, padding='post')
    predictions = model.predict(padded_input)[0]
    intent_idx = np.argmax(predictions)
    confidence = predictions[intent_idx]
    intent_label = le.inverse_transform([intent_idx])[0]
    return intent_label, confidence

from datetime import datetime

def save_prompt(user_input):
    try:
        prompt_data = {
            "prompt": user_input,
            "timestamp": datetime.now()
        }
        prompts_collection.insert_one(prompt_data)
        print(f"Prompt saved: {user_input}")
    except Exception as e:
        print(f"Error saving prompt: {e}")

def convert_to_html(text):
    """
    Convert plain text with markdown-like syntax to HTML.
    
    Replace * text with <li>text</li>
    """
    # Replace **text** with <strong>text</strong>
    text = text.replace('**', '<strong>', 1)
    text = text.replace('**', '</strong>', 1)

    lines = text.split('\n')
    html_lines = []
    for line in lines:
        if line.strip().startswith('* '):
            line = f"<li>{line[2:].strip()}</li>"
        html_lines.append(line)
    text = '\n'.join(html_lines)

    
    if '<li>' in text:
        text = text.replace('<li>', '<ul><li>', 1)
        text = text.replace('</li>', '</li></ul>', text.count('</li>') - 1)

    text = text.replace('\n', '<br>')

    return text


@app.post("/chatbot")
def chatbot(request: ChatRequest):
    user_input = request.message.strip()

    save_prompt(user_input)

    if user_input == "./dev":
        return {"response": "Enter admin username and password as 'username,password'."}

    intent_label, confidence = predict_intent(user_input)

    # If confidence is high, return intent-based response
    CONFIDENCE_THRESHOLD = 0.99555
    if confidence >= CONFIDENCE_THRESHOLD:
        response = next(
            (random.choice(intent['responses']) for intent in data['intents'] if intent['intent'] == intent_label),
            "I'm sorry, I don't have an answer for that."
        )
        if not any(tag in response for tag in ['<strong>', '<ul>', '<li>', '<br>']):
            response = convert_to_html(response)
        return {"response": response}

    # Admin login logic : "./dev"
    if "," in user_input and " " not in user_input:
        username, password = user_input.split(",", 1)
        admin = admin_collection.find_one({"username": username, "password": password})
        if admin:
            admin_sessions[username] = True
            return {"response": "Login successful."}
        else:
            return {"response": "Invalid admin credentials."}
        
    if user_input.lower() == "view prompts":
        for username in admin_sessions:
            if admin_sessions.get(username, False):
                prompts = list(prompts_collection.find({}, {"_id": 0, "prompt": 1}))
                return {"response": prompts}
        return {"response": "You must log in as an admin to view prompts."}

    # If confidence is low, use Groq API for response
    try:
        response = groq_response(user_input)
    except Exception:
        response = "I'm sorry, I couldn't process your question."

    return {"response": response}

def chatbot(request: ChatRequest):
    user_input = request.message.strip()

    
    if user_input == "./dev":
        return {"response": "Enter admin username and password as 'username,password'."}

    
    intent_label, confidence = predict_intent(user_input)


    CONFIDENCE_THRESHOLD = 0.99555
    if confidence >= CONFIDENCE_THRESHOLD:
        response = next(
            (random.choice(intent['responses']) for intent in data['intents'] if intent['intent'] == intent_label),
            "I'm sorry, I don't have an answer for that."
        )
        return {"response": response}

    if "," in user_input and " " not in user_input:
        username, password = user_input.split(",", 1)
        admin = admin_collection.find_one({"username": username, "password": password})
        if admin:
            admin_sessions[username] = True
            return {"response": "Login successful."}
        else:
            return {"response": "Invalid admin credentials."}
        
    if user_input.lower() == "view prompts":
        for username in admin_sessions:
            if admin_sessions.get(username, False):
                prompts = list(prompts_collection.find({}, {"_id": 0, "prompt": 1}))
                return {"response": prompts}
        return {"response": "You must log in as an admin to view prompts."}

   
    try:
        response = groq_response(user_input)
    except Exception:
        response = "I'm sorry, I couldn't process your question."

    return {"response": response}




@app.post("/admin/login")
def admin_login(credentials: AdminCredentials):
    admin = admin_collection.find_one({"username": credentials.username, "password": credentials.password})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/admin/prompts")
def get_prompts(username: str, password: str):
    admin = admin_collection.find_one({"username": username, "password": password})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    prompts = list(prompts_collection.find({}, {"_id": 0, "prompt": 1}))
    return {"prompts": prompts}


ngrok.set_auth_token("your-auth-token")
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
