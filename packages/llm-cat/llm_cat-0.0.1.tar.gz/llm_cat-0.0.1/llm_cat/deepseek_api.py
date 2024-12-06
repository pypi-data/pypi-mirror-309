import requests


def deepseek_chat(message,token):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token  # Replace with your actual API key
    }
    data = {
        "model": "deepseek-chat",
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None





