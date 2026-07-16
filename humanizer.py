from ollama import chat


def humanize_text(text):
    prompt = f"""
You are an expert writing assistant.

Rewrite the following text so it sounds naturally written by a human.

Rules:
- Keep the original meaning.
- Improve flow.
- Vary sentence lengths.
- Remove repetitive wording.
- Don't add new information.
- Return only the rewritten text.

Text:
{text}
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]