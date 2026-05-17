import uuid

from qdrant_client.models import (
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from app.rag.qdrant_client import (
    client
)

from app.rag.setup_qdrant import (
    COLLECTION_NAME
)

def store_chunks(
    embeddings,
    chunks,
    file_id
):

    points = []

    for embedding, chunk in zip(
        embeddings,
        chunks
    ):

        points.append(

            PointStruct(
                id=str(uuid.uuid4()),

                vector=embedding.tolist(),

                payload={
                    "text": chunk,
                    "file_id": file_id
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search_chunks(
    query_embedding,
    file_id=None,
    limit=3
):
    query_filter = None
    if file_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="file_id",
                    match=MatchValue(value=file_id)
                )
            ]
        )

    response = client.query_points(
        collection_name=COLLECTION_NAME,

        query=query_embedding.tolist(),

        limit=limit,

        query_filter=query_filter
    )

    return [
        result.payload["text"]
        for result in response.points
    ]