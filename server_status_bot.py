import time
import psutil
import requests
import GPUtil
from dateutil import parser
import json
import os

# Load credentials and webhooks from secrets.json
with open('secrets.json', 'r') as f:
    secrets = json.load(f)

SLACK_WEBHOOK_URL = secrets['slack_webhook_url']


def get_system_status():
    """Fetch system metrics: CPU, GPU utilization, and Ollama ps call."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    ram_usage = memory_info.percent

    gpus = GPUtil.getGPUs()
    gpu_status = []
    for gpu in gpus:
        gpu_status.append(f"GPU {gpu.id}: {gpu.load * 100:.2f}%")
        gpu_status.append(f"GPU {gpu.id} VRAM Usage: {gpu.memoryUtil * 100:.2f}%")

    gpu_message = "\n".join(gpu_status) if gpu_status else "No GPU detected."

    # Integrate Ollama ps call
    try:
        ollama_response = requests.get("http://localhost:11434/api/ps")
        if ollama_response.status_code == 200:
            ollama_data = ollama_response.json()
            models = ollama_data.get("models", [])
            if models:
                ollama_message = "*Ollama Status:*\n"
                for model in models:
                    expring_timestamp = model.get('expires_at', 'N/A')
                    if expring_timestamp != 'N/A':
                        expring_timestamp = parser.parse(expring_timestamp).timestamp()

                    expires_in = "N/A"
                    if expring_timestamp != 'N/A':
                        expires_in = time.strftime("%H:%M:%S", time.gmtime(expring_timestamp - time.time()))

                    ollama_message += (
                        f"- Model Name: {model.get('name', 'N/A')}\n"
                        f"  Parameter Size: {model.get('details', {}).get('parameter_size', 'N/A')}\n"
                        f"  VRAM Usage: {model.get('size_vram', 'N/A') / (1024**3):.2f} GB\n"
                        f"  Quantization Level: {model.get('details', {}).get('quantization_level', 'N/A')}\n"
                        f"  Expires At: {model.get('expires_at', 'N/A')}\n"
                        f" Exprires In: {expires_in}\n"
                    )
            else:
                ollama_message = "Ollama Status: No models found."
        else:
            ollama_message = f"Ollama API Error: {ollama_response.status_code}"
    except requests.RequestException as e:
        ollama_message = f"Ollama API Exception: {e}"

    return f"*Server Status*\nCPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%\n{gpu_message}\n{ollama_message}"

def send_to_slack(message):
    """Send system status to Slack."""
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

if __name__ == "__main__":
    while True:
        status_message = get_system_status()
        print(status_message)
        send_to_slack(status_message)
        time.sleep(300)  # Sends update every 5 minutes
