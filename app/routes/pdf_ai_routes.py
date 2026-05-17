import os
import uuid
import requests

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.file import File

from app.rag.embedder import (
    create_embedding
)

from app.rag.vector_store import (
    vector_store
)

from app.rag.pdf_processor import (
    extract_pdf_text,
    chunk_text
)

from app.rag.rag_chat import (
    ask_pdf_question
)
from app.rag.qdrant_store import (
    store_chunks
)

from app.rag.qdrant_store import (
    search_chunks
)

router = APIRouter(
    prefix="/pdf-ai",
    tags=["PDF AI"]
)

@router.post("/process/{file_id}")
def process_pdf(
    file_id: int,
    db: Session = Depends(get_db)
):

    file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not file:
        return {
            "error": "File not found"
        }

    temp_path = f"temp/{uuid.uuid4()}.pdf"

    os.makedirs("temp", exist_ok=True)

    response = requests.get(
        file.file_url
    )

    with open(temp_path, "wb") as f:
        f.write(response.content)

    text = extract_pdf_text(
        temp_path
    )

    chunks = chunk_text(text)

    embeddings = create_embedding(
        chunks
    )

    store_chunks(
        embeddings,
        chunks,
        file_id
    )

    os.remove(temp_path)

    return {
        "message": "PDF processed successfully"
    }

@router.post("/chat")
def chat_with_pdf(payload: dict):

    question = payload.get(
        "question"
    )

    file_id = payload.get("file_id")

    query_embedding = create_embedding(
        [question]
    )[0]

    relevant_chunks = search_chunks(
        query_embedding,
        file_id
    )

    answer = ask_pdf_question(
        relevant_chunks,
        question
    )

    return {
        "answer": answer,
        "context": relevant_chunks
    }