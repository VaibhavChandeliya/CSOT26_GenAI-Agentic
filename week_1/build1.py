import os
from openai import OpenAI
from dotenv import load_dotenv

# Manually point to the .env file path inside your folder structure
load_dotenv(dotenv_path="./CSOT26_GenAI-Agentic/.env")

# The key is now safely loaded from your environment, keeping it secret!
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def call_model(prompt: str) -> str:
    """
    Make a single chat completion call.
    Print the full response object first and understand its structure.
    Then return just the assistant's text.
    """
    response = client.chat.completions.create(
        model="openrouter/free", 
        messages=[
            {"role": "system", "content": "You are a helpful and concise assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    
    # TODO: inspect `response` before you extract anything from it
    print("\n================ FULL RESPONSE OBJECT ================")
    print(response)
    print("======================================================\n")
    
    # TODO: What's in response.choices? What's in response.usage?
    print("--- Inspecting Fields ---")
    print(f"Content of response.choices:\n{response.choices}\n")
    print(f"Content of response.usage:\n{response.usage}\n")
    print("-------------------------\n")
    
    # Return just the assistant's clean text
    return response.choices[0].message.content

if __name__ == "__main__":
    print(call_model("What is the capital of India?"))