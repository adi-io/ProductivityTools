import requests
import pyperclip
import os
import re
import time

# Function to remove markdown and clean text
def remove_markdown(text):
    text = re.sub(r'^\s*#+\s*', '', text, flags=re.MULTILINE)  # Remove markdown headings
    text = re.sub(r'\*\*|\*|__|_', '', text)  # Remove bold/italic markers
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)  # Remove bullet points
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # Remove numbered lists
    text = re.sub(r'^\s*\d+\)\s+', '', text, flags=re.MULTILINE)  # Remove numbered lists with )
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

def handle_clipboard_content():
    previous_content = None

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

    openai_api_endpoint = "https://api.openai.com/v1/chat/completions"
    openai_model = "gpt-3.5-turbo"  # or another model

    while True:
        current_content = pyperclip.paste()

        if current_content and current_content != previous_content:
            try:
                openai_payload = {
                    "model": openai_model,
                    "messages": [
                        {"role": "system", "content": "ADD YOUR PROMPT HERE"},
                        {"role": "user", "content": current_content}
                    ],
                    "max_tokens": 4000,
                    "temperature": 0.7
                }

                # Call OpenAI API
                openai_response = requests.post(openai_api_endpoint, headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_api_key}"
                }, json=openai_payload)

                if openai_response.status_code == 200:
                    openai_data = openai_response.json()
                    gpt_response_text = openai_data['choices'][0]['message']['content'].strip()

                    cleaned_response = remove_markdown(gpt_response_text)

                    pyperclip.copy(cleaned_response)
                    previous_content = cleaned_response

                    print("Updated Clipboard with Cleaned Response:", cleaned_response)
                else:
                    print(f"Failed to get a response from OpenAI API: {openai_response.status_code} - {openai_response.text}")

            except Exception as e:
                print(f"An error occurred: {e}")

        time.sleep(5)  # Wait for 5 seconds before checking clipboard again

if __name__ == "__main__":
    try:
        print("Monitoring clipboard content. Press Ctrl+C to stop.")
        handle_clipboard_content()
    except KeyboardInterrupt:
        print("Stopped monitoring clipboard content.")
    except Exception as e:
        print(f"An error occurred during execution: {e}")

