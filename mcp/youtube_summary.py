import re
import requests
from youtube_transcript_api._api import YouTubeTranscriptApi

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def fetch_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return "❌ Invalid YouTube URL."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return full_text
    except Exception as e:
        return f"❌ Error fetching transcript: {e}"

def summarize_transcript(transcript, llm_url, model_path, max_tokens, temperature):
    payload = {
        "model": model_path,
        "messages": [
            {"role": "system", "content": "Summarize the following YouTube transcript briefly."},
            {"role": "user", "content": transcript}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(llm_url, json=payload)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ LLM error: {e}"

def summarize_youtube_video(video_url, llm_config):
    transcript = fetch_transcript(video_url)
    if transcript.startswith("❌"):
        return transcript
    return summarize_transcript(
        transcript,
        llm_config["url"],
        llm_config["model_path"],
        llm_config["max_tokens"],
        llm_config["temperature"]
    )
