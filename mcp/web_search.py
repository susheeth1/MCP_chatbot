# mcp/web_search.py
import requests
import json

def web_search(query, config):
    if not config["serper"]["enabled"]:
        return ""

    try:
        response = requests.post(
            config["serper"]["url"],
            headers={
                "X-API-KEY": config["serper"]["api_key"],
                "Content-Type": "application/json"
            },
            data=json.dumps({"q": query})
        )
        response.raise_for_status()
        results = response.json().get("organic", [])
        context = "\n".join(f"{r['title']}: {r.get('snippet', '')}" for r in results[:3])
        return context
    except Exception as e:
        return f"❌ Web search failed: {e}"
