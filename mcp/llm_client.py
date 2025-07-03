# mcp/llm_client.py
import requests
import json

def call_llm(prompt, config, system_prompt="", context=None):
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    full_prompt = f"{context}\n{prompt}" if context else prompt
    messages.append({"role": "user", "content": full_prompt})

    payload = {
        "model": config["llm"]["model_path"],
        "messages": messages,
        "max_tokens": config["llm"]["max_tokens"],
        "temperature": config["llm"]["temperature"]
    }

    try:
        response = requests.post(
            config["llm"]["url"],
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ LLM error: {e}"
