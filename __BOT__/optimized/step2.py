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

# Load tokenizer
with open('tokenizer.json') as f:
    tokenizer_data = json.load(f)
tokenizer = tokenizer_from_json(tokenizer_data)

# Load label encoder
with open('label_encoder.json') as f:
    label_classes = json.load(f)
le = LabelEncoder()
le.classes_ = np.array(label_classes)

# Load intents dataset
with open('extracted/intents.json') as file:
    data = json.load(file)

max_len = model.input_shape[1]

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
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
os.environ["GROQ_API_KEY"] = "your api key here"

def groq_response(user_input):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY is not set."

    client = Groq(api_key=api_key)
    system_prompt = {
        "role": "assistant",
        "content": "You are a helpful assistant. The college name is IEM Kolkata. Provide relevant answers."
    }

    chat_history = [system_prompt, {"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=250,
        temperature=1.2
    )
    return response.choices[0].message.content

def predict_intent(user_input):
    encoded_input = tokenizer.texts_to_sequences([user_input])
    padded_input = pad_sequences(encoded_input, maxlen=max_len, padding='post')
    predictions = model.predict(padded_input)[0]
    intent_idx = np.argmax(predictions)
    confidence = predictions[intent_idx]
    intent_label = le.inverse_transform([intent_idx])[0]
    return intent_label, confidence

@app.post("/chatbot")
def chatbot(request: ChatRequest):
    user_input = request.message.strip()

    if user_input == "./dev":
        return {"response": "Enter admin username and password as 'username,password'."}

    if "," in user_input:
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
        return {"response": "You must log in as an admin."}

    CONFIDENCE_THRESHOLD = 0.99555
    prompts_collection.insert_one({"prompt": user_input})
    intent_label, confidence = predict_intent(user_input)

    if confidence < CONFIDENCE_THRESHOLD:
        try:
            response = groq_response(user_input)
        except Exception:
            response = "I'm sorry, I couldn't process your question."
    else:
        response = next(
            (random.choice(intent['responses']) for intent in data['intents'] if intent['intent'] == intent_label),
            "I'm sorry, I don't have an answer for that."
        )
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

# Expose FastAPI with ngrok
ngrok.set_auth_token("api key here")
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
