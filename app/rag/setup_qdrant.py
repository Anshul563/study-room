from qdrant_client.models import (
    VectorParams,
    Distance
)

from app.rag.qdrant_client import (
    client
)

COLLECTION_NAME = "study_room_docs"

def create_collection():

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Qdrant collection created")