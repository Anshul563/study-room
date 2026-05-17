from groq import Groq

from app.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)

def generate_room_summary(messages: list):

    if not messages:
        return "No discussion found."

    formatted_chat = "\n".join(messages)

    prompt = f"""
    You are an AI study assistant.

    Create clean study notes from this discussion.

    Requirements:
    - Short summary
    - Important concepts
    - Key learning points
    - Simple explanation
    - Student friendly

    Discussion:
    {formatted_chat}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=500
    )

    return response.choices[0].message.content