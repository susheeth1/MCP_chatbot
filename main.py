# main.py
import json
from mcp.llm_client import call_llm
from mcp.web_search import web_search

# Load config
with open('config.json') as f:
    config = json.load(f)

print("\n🤖 Welcome to your Command-Line AI Chatbot!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("🧑 You: ")

    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    context = web_search(user_input, config)
    response = call_llm(user_input, config, context=context)
    
    print(f"🤖 Bot: {response}\n")
