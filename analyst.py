from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert document analyst. You are given extracted 
content from a PDF document including text and tables. Your job is to answer 
questions about the document clearly and accurately.

Rules:
- Only answer based on what is in the document
- If something is not in the document, say so clearly
- For numbers and data, be precise
- Keep answers concise but complete
- If tables are present, use them to answer data questions
"""


def format_tables_as_text(tables: list) -> str:
    """Convert extracted tables into readable text for the prompt."""
    if not tables:
        return ""
    
    result = "\n\n--- TABLES FOUND IN DOCUMENT ---\n"
    for i, table in enumerate(tables):
        result += f"\nTable {i+1} (Page {table['page']}):\n"
        for row in table["data"]:
            cleaned_row = [str(cell) if cell else "" for cell in row]
            result += " | ".join(cleaned_row) + "\n"
    return result


def build_context(extracted: dict, max_chars: int = 100000) -> str:
    """Build the full context string from extracted PDF content."""
    context = "--- DOCUMENT TEXT ---\n"
    context += extracted["text"]
    context += format_tables_as_text(extracted["tables"])

    # Truncate if too large for context window
    if len(context) > max_chars:
        context = context[:max_chars]
        context += "\n\n[Document truncated due to length]"

    return context


def ask_question(question: str, extracted: dict, chat_history: list) -> str:
    """Send question + document context to GPT-4o and stream the answer."""
    context = build_context(extracted)

    # Build messages list
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here is the document content:\n\n{context}"},
        {"role": "assistant", "content": "I have read the document. What would you like to know?"},
    ]

    # Add previous chat history
    for msg in chat_history:
        messages.append(msg)

    # Add current question
    messages.append({"role": "user", "content": question})

    # Stream the response
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end="", flush=True)

    print()  # newline after streamed response
    return full_response


def summarise_document(extracted: dict) -> str:
    """Generate a quick summary of the document."""
    context = build_context(extracted)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Please provide a concise summary of this document in 3-5 sentences:\n\n{context}"}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

