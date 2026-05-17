import faiss
import numpy as np

class VectorStore:

    def __init__(self):

        self.dimension = 384

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.text_chunks = []

    def add_embeddings(
        self,
        embeddings,
        chunks
    ):

        embeddings = np.array(
            embeddings
        ).astype("float32")

        self.index.add(embeddings)

        self.text_chunks.extend(chunks)

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        query_embedding = np.array(
            [query_embedding]
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx >= 0 and idx < len(self.text_chunks):

                results.append(
                    self.text_chunks[idx]
                )

        return results

vector_store = VectorStore()