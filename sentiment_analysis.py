import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")


client = Groq(api_key=api_key)

with open("students_feedback.json", "r") as file:
    responses = json.load(file)


all_responses = " ".join(response["text"] for response in responses)

response_emojis = [
    '😊' ,
    '😡' ,
    '🤩' ,
    '😐' ,
    '☹️' ,
    '😑'
]
prompt = (
    f"You are an efficient , experienced and highly capable sentiment analyzer. Your task is to accurately analyze the following student feedback responses "
    f"and summarize the overall sentiment in one word. Keep it mind always try to give the most relevant answer as per the input, make proper analysis "
    f"of input, never give multiple responses just analyze properly and give most deserving output. Never give an ambiguous answer, always give a "
    f"straightforward and accurate answer. Please ensure to provide the most relevant answer based on the input, and choose an appropriate emoji from the "
    f"following list based on your final response: {response_emojis}. Also, find out the exact percentage of good, bad, and neutral responses based on the input. "
    f"Here are the responses: {all_responses}"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama3-8b-8192",
)

output = chat_completion.choices[0].message.content

with open("output.md", "w" , encoding="utf-8") as file:
    file.write(output)

print("Summary written to output.md")
