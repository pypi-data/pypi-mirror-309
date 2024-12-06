import requests

def ollama_chat(content,model='llama3.1',url = 'http://localhost:11434/api/chat'):
    """
    发送聊天请求并返回响应结果。

    Args:
        model (str): 指定的模型。
        messages (list[dict]): 包含聊天信息的字典列表。

    Returns:
        dict: 包含响应结果的字典。
    """

    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    # 定义请求体参数
    data = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json=data)
        # 检查响应状态码
        response.raise_for_status()
        # 返回响应的 JSON 内容
        return response.json()['message']['content']

    except requests.exceptions.RequestException as e:
        print(f"Failed to send chat request: {e}")
        return None

