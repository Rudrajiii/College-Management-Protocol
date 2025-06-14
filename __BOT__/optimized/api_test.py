import requests

url = "https://b381-2409-40e0-2b-64f4-e531-7cb0-cdea-6620.ngrok-free.app/chatbot"
headers = {"Content-Type": "application/json"}

while True:
    user_input = input("Enter your message (type 'finish' to exit): ")

    if user_input.lower() == "finish":
        print("Exiting chatbot. Goodbye!")
        break

    payload = {"message": user_input}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if "Enter admin username and password" in response_data.get("response", ""):
            print("Chatbot:", response_data["response"])
            admin_input = input("Enter admin username and password: ")
            admin_payload = {"message": admin_input}
            admin_response = requests.post(url, json=admin_payload, headers=headers)
            print("Chatbot:", admin_response.json().get("response", "No response received"))

        elif isinstance(response_data.get("response"), list):
            print("Saved Prompts:")
            for prompt in response_data["response"]:
                print(f"- {prompt['prompt']}")

        else:
            print("Chatbot:", response_data.get("response", "No response received"))

    except Exception as e:
        print(f"Error communicating with the chatbot: {e}")
