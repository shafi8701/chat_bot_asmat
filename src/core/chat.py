from src.config.settings import settings
from src.core.prompts import WELCOME

def run_chat():
    print(WELCOME.format(name=settings.BOT_NAME))
    
    while True:
        user = input("> ").strip()

        if user.lower() in {"exit", "quit", "q"}:
            print("Bye!")
            break

        # Placeholder response (replace with LLM/API call)
        print(f"Echo: {user}")