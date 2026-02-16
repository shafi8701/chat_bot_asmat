from src.config.settings import settings
from src.core.prompts import WELCOME
from src.services.rag_service import RAGService

def run_chat():
    print(WELCOME.format(name=settings.BOT_NAME))

    rag = RAGService()

    while True:
        user = input("> ").strip()

        if user.lower() in {"exit", "quit", "q"}:
            print("Bye!")
            break

        # 🔥 Instead of echo
        response = rag.generate(user)
        print(response)