from phi.embedder.openai import OpenAIEmbedder
from phi.vectordb.pineconedb import PineconeDB
from pinecone.grpc import PineconeGRPC as Pinecone
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.json import JSONKnowledgeBase

model_embedd_openai = OpenAIEmbedder(model="text-embedding-3-small")

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_5stbCS_gLGYTCEU1FyVrrRATX5HMPKBWTyN7bAxyiQbyLUzRb2q2LaUZDjd74q8oYhWVr")
api_key="pcsk_5stbCS_gLGYTCEU1FyVrrRATX5HMPKBWTyN7bAxyiQbyLUzRb2q2LaUZDjd74q8oYhWVr"

# Gantilah PineconeDB untuk penggunaan vektor di database Pinecone
class KnowledgeBaseRepository:
    def __init__(self):
        # Inisialisasi PineconeDB untuk pdf dan json knowledge
        self.vector_db_pdf = PineconeDB(
            name="product-information-hybrid-search",
            dimension=1536,  # Sesuaikan dimensi dengan embedding model Anda
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
            api_key=api_key,  # Ganti dengan API Key Anda
            use_hybrid_search=True,
            hybrid_alpha=0.5,
            embedder=model_embedd_openai,
        )
        
        self.vector_db_json = PineconeDB(
            name="document-complaint-hybrid-search",
            dimension=1536,  # Sesuaikan dimensi dengan embedding model Anda
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
            api_key=api_key,  # Ganti dengan API Key Anda
            use_hybrid_search=True,
            hybrid_alpha=0.5,
            embedder=model_embedd_openai,
        )
        
        # Knowledge Base ini berisi data PDF dan JSON
        self.pdf_knowledge = PDFKnowledgeBase(
            path="app/resources/", 
            vector_db=self.vector_db_pdf, reader=PDFReader(chunk=True)
        )
        
        self.json_knowledge = JSONKnowledgeBase(
            path="app/resources/", 
            vector_db=self.vector_db_json
        )

    # def load_knowledge(self, recreate=False, upsert=True):
    #     # Memuat pengetahuan dari PDF dan JSON ke dalam database Pinecone
    #     self.pdf_knowledge.load(recreate=recreate, upsert=upsert)
    #     self.json_knowledge.load(recreate=recreate, upsert=upsert)
