from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

class PineconeService:
    def __init__(self):
        self.pc = None
        self.index = None
        if settings.PINECONE_API_KEY:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Create index if it doesn't exist
            if settings.PINECONE_INDEX_NAME not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=128, # face_recognition uses 128d embeddings
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.PINECONE_ENV
                    )
                )
            
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)

    def upsert_face(self, user_id: str, embedding: list[float]):
        if not self.index:
            print(f"Mock upsert for {user_id}")
            return
        
        self.index.upsert(
            vectors=[
                {"id": user_id, "values": embedding, "metadata": {"user_id": user_id}}
            ]
        )

    def verify_face(self, embedding: list[float], threshold: float = 0.90):
        if not self.index:
            print("Mock verify: returning unknown")
            return None, 0.0

        query_res = self.index.query(
            vector=embedding,
            top_k=1,
            include_metadata=True
        )

        if query_res.matches and len(query_res.matches) > 0:
            best_match = query_res.matches[0]
            if best_match.score >= threshold:
                return best_match.metadata.get("user_id"), best_match.score
            
        return None, (query_res.matches[0].score if query_res.matches else 0.0)

pinecone_service = PineconeService()
