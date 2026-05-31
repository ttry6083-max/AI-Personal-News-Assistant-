import json
import os
from dotenv import load_dotenv

import news_helper
import ai_helper
import email_helper
import memory

load_dotenv()

with open("config.json") as f:
    config = json.load(f)

SEND_TO_EMAIL = os.getenv("SEND_TO_EMAIL")


def run():
    print("\n=== Your Personal News Assistant ===")
    print("Commands: 'clear' to reset memory | 'quit' to exit")
    print("Just talk to me naturally.\n")

    service = email_helper.authenticate()
    conversation_history, last_digest = memory.load_memory()

    if conversation_history:
        print(f"Assistant: Welcome back! I remember our last conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Assistant: See you later!")
            break

        if user_input.lower() == "clear":
            memory.clear_memory()
            conversation_history = []
            last_digest = None
            continue

        conversation_history.append({"role": "user", "content": user_input})

        email_words = ["send", "email", "mail", "inbox"]
        wants_email = any(word in user_input.lower() for word in email_words)

        action = ai_helper.decide_action(conversation_history)

        if action["type"] == "fetch_news":
            category = action.get("category", "general")
            country = action.get("country", "")
            articles = news_helper.get_top_news(
                category=category,
                country=country,
                num_articles=config["num_articles"]
            )
            if not articles:
                response = "Sorry, I couldn't find any news right now. Try again!"
            else:
                last_digest = ai_helper.summarize_news(articles)
                response = action["response"] + "\n\n" + last_digest
                if wants_email and last_digest:
                    email_helper.send_digest(service, last_digest, SEND_TO_EMAIL)
                    response += "\n\nI've also sent this to your inbox!"

        elif action["type"] == "send_email" or (wants_email and last_digest):
            if last_digest:
                email_helper.send_digest(service, last_digest, SEND_TO_EMAIL)
                response = "Done! Just sent it to your inbox. Go check it!"
            else:
                response = "I haven't fetched any news yet! Ask me what you'd like to read first."

        else:
            response = action["response"]

        print(f"\nAssistant: {response}\n")
        conversation_history.append({"role": "assistant", "content": response})

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        memory.save_memory(conversation_history, last_digest)


if __name__ == "__main__":
    run()
