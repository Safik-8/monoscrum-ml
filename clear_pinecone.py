from app.services.pinecone_service import pinecone_service

try:
    pinecone_service.index.delete(delete_all=True)
    print("Successfully cleared all faces from Pinecone!")
except Exception as e:
    print(f"Error: {e}")
