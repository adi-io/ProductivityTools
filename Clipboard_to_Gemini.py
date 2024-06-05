import pyperclip
import requests
import os
import re
import google.generativeai as genai
import time

# Configure API key for Generative AI
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print("API_KEY environment variable is not set.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Function to clean up bullet points and markdown formatting
def remove_markdown(text):
    text = re.sub(r'^\s*#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*|\*|__|_', '', text)
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\)\s+', '', text, flags=re.MULTILINE)
    return text

previous_output = None

def handle_clipboard_content():
    global previous_output

    current_content = pyperclip.paste()

    # Check if the current content is the same as the previously handled output
    if current_content and current_content != previous_output:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')

            prompt = "ADD YOUR PROMPT HERE"
            response = model.generate_content(prompt + current_content)

            if response and response.candidates:
                gemini_output = response.candidates[0].content.parts[0].text
                output = remove_markdown(gemini_output)
                print(f"Gemini Output: {output}")  # Log Gemini output
                previous_output = output
                pyperclip.copy(output)
            else:
                print("No candidates found in Gemini response.")

        except Exception as e:
            print(f"An error occurred: {e}")  # Log any errors

# Main loop to monitor clipboard content
print("Monitoring clipboard content. Press Ctrl+C to stop.")

try:
    while True:
        handle_clipboard_content()
        time.sleep(5)  # Check the clipboard every 5 seconds
except KeyboardInterrupt:
    print("Stopped monitoring clipboard content.")
except Exception as e:
    print(f"An error occurred during execution: {e}")
    sys.exit(1)

