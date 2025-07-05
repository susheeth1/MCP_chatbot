import json
from mcp.llm_client import call_llm
from mcp.web_search import web_search
from mcp.youtube_summary import summarize_youtube_video


with open("config.json") as f:
    config = json.load(f)

print("🤖 Welcome to your Command-Line AI Chatbot!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("🧑 You: ")
    if user_input.lower() == "exit":
        break


    # 🎥 YouTube Summary
    if "youtube.com" in user_input or "youtu.be" in user_input:
        response = summarize_youtube_video(user_input, config["llm"])
        print(f"\n🤖 Bot: {response}\n")
        continue

    # 🔎 Web Search (Serper)
    context = ""
    if config.get("serper", {}).get("enabled"):
        context = web_search(user_input, config["serper"])

    # 🤖 LLM Response
    response = call_llm(user_input, context, config["llm"])
    print(f"\n🤖 Bot: {response}\n")
