import os
import sys
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-haiku-4-5-20251001"

# Sample details: replace them with your SACCO's real ones.
SYSTEM_PROMPT = """You are the member assistant for Thika Matatu SACCO.
Answer in 2 to 3 short, friendly sentences. Reply in the language the member uses (English or Swahili).

Use only these facts:
1. Balance: You cannot see individual balances. Ask the member to send their member number to the secretary on 0700 000 000. She replies within one working day.
2. Next meeting: Saturday 7 November 2026, 10:00 AM, at the SACCO office in Thika.
3. Membership fees: Registration is KES 1,000, paid once. The monthly contribution is KES 2,000, due by the 5th of each month. Pay by M-Pesa Paybill 000000, using the member number as the account number.

If the question is about anything else, say you can only help with balances, meetings and fees, and ask the member to call the secretary on 0700 000 000.
Never guess or invent amounts, dates or balances."""

TEST_QUESTIONS = [
    "What is my balance?",
    "How much money do I have in my account?",
    "Nataka kujua salio langu",
    "When is the next meeting?",
    "hey when do we meet next",
    "Mkutano ujao ni lini?",
    "What are the current membership fees?",
    "How much do I pay every month to stay a member?",
    "What does it cost to join?",
    "Can I get a loan to buy a new matatu?",
]


def ask(question):
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}],
        )
        return message.content[0].text
    except anthropic.APIConnectionError:
        return "No internet connection. Check your connection and try again."
    except anthropic.AuthenticationError:
        return "API key is wrong or expired. Check your .env file."
    except anthropic.RateLimitError:
        return "Too many requests. Wait 60 seconds and try again."
    except anthropic.BadRequestError as error:
        return f"The API rejected the request: {error.message}"
    except anthropic.APIStatusError as error:
        return f"The API returned an error: {error.status_code}"


if len(sys.argv) > 1 and sys.argv[1] == "--test":
    for question in TEST_QUESTIONS:
        print(f"Q: {question}")
        print(f"A: {ask(question)}\n")
else:
    print("Matatu SACCO Assistant (type 'quit' to stop)\n")
    while True:
        question = input("Member question: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if question:
            print(f"\n{ask(question)}\n")