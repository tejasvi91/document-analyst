from extractor import extract_all

# Read any PDF you have on your computer
with open("sample.pdf", "rb") as f:
    pdf_bytes = f.read()

result = extract_all(pdf_bytes)

print(f"Text length   : {result['stats']['text_length']} characters")
print(f"Tables found  : {result['stats']['table_count']}")
print(f"Images found  : {result['stats']['image_count']}")
print("\nFirst 500 characters of text:")
print(result['text'][:500])


from analyst import ask_question, summarise_document

print("\n--- DOCUMENT SUMMARY ---")
summary = summarise_document(result)
print(summary)

print("\n--- ASK A QUESTION ---")
answer = ask_question(
    "What is this person's work experience?",
    result,
    chat_history=[]
)