from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic()

def generate_question(notes:str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Based on the following study notes, generate one clear question that tests deep understanding. Only return the question, nothing else. \n\nNotes: {notes}"
            }
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    notes = input("Paste your study notes here: ")
    question = generate_question(notes)
    print("\nYour study question:")
    print(question)