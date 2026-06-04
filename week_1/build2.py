import os
from openai import OpenAI
from dotenv import load_dotenv

# Manually point to your .env file inside your folder structure
load_dotenv(dotenv_path="./CSOT26_GenAI-Agentic/.env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def run_chatbot():
    """
    A terminal chatbot that holds a coherent multi-turn conversation.
    - Maintains conversation history in a list.
    - Includes '/reset' command to clear context.
    - Includes '/tokens' command to track performance.
    """
    # Start with a system message to set the AI's behavior
    messages = [
        {"role": "system", "content": "You are a helpful and concise assistant."}
    ]

    print("====================================================")
    print("🤖 Chatbot initialized! Type your prompt to begin.")
    print("💡 Commands: Type 'exit' to quit, '/reset' to clear memory, '/tokens' for stats.")
    print("====================================================\n")

    # Tracking variable for the stretch goals
    last_usage_stats = None

    while True:
        # 1. Take user input
        user_input = input("You: ").strip()
        
        # Check if the user entered an empty prompt
        if not user_input:
            continue

        # Check for exit commands
        if user_input.lower() in ['exit', 'quit']:
            print("\nGoodbye! Ending session.")
            break

        # STRETCH GOAL 1: Handle '/reset' command
        if user_input.lower() == '/reset':
            messages = [
                {"role": "system", "content": "You are a helpful and concise assistant."}
            ]
            last_usage_stats = None
            print("\n🧹 [System: Memory cleared! The AI has forgotten everything.]\n")
            continue

        # STRETCH GOAL 2: Handle '/tokens' command
        if user_input.lower() == '/tokens':
            print("\n📊 [Token Usage Breakdown for last call]:")
            if last_usage_stats:
                print(f"  - Prompt (Input) Tokens: {last_usage_stats.prompt_tokens}")
                print(f"  - Completion (Output) Tokens: {last_usage_stats.completion_tokens}")
                print(f"  - Total Tokens Transferred: {last_usage_stats.total_tokens}\n")
            else:
                print("  - No API calls have been made yet in this session.\n")
            continue
            
        # 2. Append the user turn to messages array
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 3. Call the API with the full messages list history
            response = client.chat.completions.create(
                model="openrouter/free",  # Bypasses overloaded individual queues
                messages=messages
            )
            
            # 4. Extract the assistant's reply text
            reply = response.choices[0].message.content
            
            # Save the usage metadata for the /tokens command
            last_usage_stats = response.usage
            
            # 5. Append the assistant turn back into the messages array
            messages.append({"role": "assistant", "content": reply})
            
            # 6. Print the reply cleanly
            print(f"\nAI: {reply}\n")
            
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")

if __name__ == "__main__":
    run_chatbot()