import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Try to find the .env file in all possible directories automatically
load_dotenv()  
current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(current_dir, ".env"))  
load_dotenv(dotenv_path=os.path.join(current_dir, "week_1", ".env"))  

class ChatAgent:
    """
    A model-agnostic ChatAgent class that handles multi-turn conversations
    using a rolling conversation buffer of size N.
    """
    def __init__(self, model_name: str = "openrouter/free", max_turns: int = 4, system_prompt: str = "You are a helpful assistant."):
        
        # Pull your API key from environment configuration fields
        api_key = os.environ.get("OPENROUTER_API_KEY")

        # 💡 EMERGENCY BACKUP: If your environment paths fail, paste your key between quotes below:
        if not api_key or api_key == "":
            api_key = "PASTE_YOUR_ACTUAL_OPENROUTER_API_KEY_HERE"

        if not api_key or "PASTE_YOUR_ACTUAL" in api_key or api_key == "":
            raise ValueError("❌ Missing credentials: API key not found in .env and not pasted manually.")

        # Establish connection client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        self.model = model_name
        self.max_turns = max_turns
        self.system_message = {"role": "system", "content": system_prompt}
        self.history_pairs = []  
        self.last_usage = None   

    def _build_payload(self) -> list:
        messages = [self.system_message]
        for user_msg, assistant_msg in self.history_pairs:
            messages.append(user_msg)
            messages.append(assistant_msg)
        return messages

    def call_model(self, user_text: str) -> str:
        current_user_msg = {"role": "user", "content": user_text}
        
        # Core Requirement: The rolling buffer memory queue pruner
        if len(self.history_pairs) >= self.max_turns:
            print(f"⚠️  [Buffer Overflow: Dropping oldest turn entry to save token space]")
            self.history_pairs.pop(0)

        temp_messages = self._build_payload()
        temp_messages.append(current_user_msg)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=temp_messages
            )
            
            reply_text = response.choices[0].message.content
            self.last_usage = response.usage
            
            current_assistant_msg = {"role": "assistant", "content": reply_text}
            self.history_pairs.append((current_user_msg, current_assistant_msg))
            
            return reply_text
        except Exception as e:
            return f"Error executing API transmission request: {e}"

    def reset_memory(self):
        self.history_pairs = []
        self.last_usage = None


# =====================================================================
# INTERACTIVE TERMINAL LOOP ENVIRONMENT
# =====================================================================
def start_interactive_session():
    print("====================================================================")
    print("🤖 Welcome to the Upgraded Class-Based ChatAgent Infrastructure!")
    print("====================================================================")
    
    print("\nSelect an LLM engine to run this session:")
    print(" [1] OpenRouter Auto-Fallback Free Routing (openrouter/free) -> RECOMMENDED")
    print(" [2] Google Gemma 2 9B Free Tier")
    print(" [3] Meta Llama 4 Scout Free Tier")
    
    choice = input("Enter choice selection number (default is 1): ").strip()
    
    # Updated 2026 live endpoints to fix the 404 errors completely
    selected_model = "openrouter/free"
    if choice == "2":
        selected_model = "google/gemma-2-9b-it:free"
    elif choice == "3":
        selected_model = "meta-llama/llama-4-scout:free"

    n_input = input("\nEnter rolling context buffer threshold length N (default is 3 pairs): ").strip()
    n_turns = int(n_input) if n_input.isdigit() else 3

    agent = ChatAgent(model_name=selected_model, max_turns=n_turns)
    
    print(f"\n✅ ChatAgent Class instantiated running model: '{selected_model}'")
    print(f"🧠 Memory Buffer tracking window configured strictly to the last N={n_turns} turns.")
    print("💡 Commands: Type 'exit' to close, '/reset' to wipe memory, '/tokens' for stats.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit']:
            print("Session closed. Goodbye!")
            break

        if user_input.lower() == '/reset':
            agent.reset_memory()
            print("\n🧹 [System Notice: Memory cleared! The agent list state was fully reset.]\n")
            continue

        if user_input.lower() == '/tokens':
            print("\n📊 [Token Metrics Log]:")
            if agent.last_usage:
                print(f"  - Prompt Input Tokens: {agent.last_usage.prompt_tokens}")
                print(f"  - Completion Generation Tokens: {agent.last_usage.completion_tokens}")
                print(f"  - Cumulative Total Session Block Transferred: {agent.last_usage.total_tokens}\n")
            else:
                print("  - No active inference executions recorded in the current stack.\n")
            continue

        ai_response = agent.call_model(user_input)
        print(f"\nAI: {ai_response}\n")

if __name__ == "__main__":
    start_interactive_session()