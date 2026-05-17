from groq import Groq

from app.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)

def ask_pdf_question(
    context_chunks,
    question
):

    context = "\n\n".join(
        context_chunks
    )

    prompt = f"""
    Answer the question ONLY
    using the provided PDF context.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,

        max_tokens=500
    )

    return response.choices[0].message.content