import pyperclip
import requests
import os
import re
import time

phrasly_api_key = os.getenv("PH")

# Function to clean up bullet points and markdown formatting
def remove_markdown(text):
    text = re.sub(r'^\s*#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*|\*|__|_', '', text)
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\)\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

phrasly_api_endpoint = "https://api.phrasly.ai/v1/humanize/"

output = pyperclip.paste()

phrasly_payload = {
    "text": output,
    "mode": "medium"
}

phrasly_response = requests.post(
    phrasly_api_endpoint,
    headers={
        "accept": "text/plain",
        "x-api-key": phrasly_api_key,
        "content-type": "application/json"
    },
    json=phrasly_payload
)

if phrasly_response.status_code == 200:
    phrasly_output = phrasly_response.text.strip()
    print(f"Phrasly Output: {phrasly_output}")  # Log Phrasly output
    phrasly_output = remove_markdown(phrasly_output)
    previous_phrasly_output = phrasly_output
    pyperclip.copy(phrasly_output)
else:
    print(f"Phrasly API request failed. Status code: {phrasly_response.status_code}")
    print(f"Response: {phrasly_response.text}")

previous_output = output

