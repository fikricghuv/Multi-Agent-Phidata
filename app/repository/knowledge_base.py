# File: knowledge_base.py
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.lancedb import LanceDb
from phi.vectordb.search import SearchType
from app.model.agent_model import model_embedd_openai

class KnowledgeBaseRepository:
    def __init__(self):
        self.vector_db_pdf = LanceDb(
            table="product_information",
            table_name="product_information",
            uri="/Users/cghuv/Documents/AGENTIC-AI-PHIDATA/app/lancedb/product_information",
            search_type=SearchType.hybrid,
            embedder=model_embedd_openai,
        )
        self.vector_db_json = LanceDb(
            table="document_complaint",
            table_name="document_complaint",
            uri="/Users/cghuv/Documents/AGENTIC-AI-PHIDATA/app/lancedb/document_complaint",
            search_type=SearchType.hybrid,
            embedder=model_embedd_openai,
        )
        self.pdf_knowledge = PDFKnowledgeBase(
            path="app/resources/", 
            vector_db=self.vector_db_pdf, reader=PDFReader(chunk=True)
        )
        self.json_knowledge = JSONKnowledgeBase(
            path="app/resources/", 
            vector_db=self.vector_db_json)

    def load_knowledge(self, recreate=True, upsert=True):
        self.pdf_knowledge.load(recreate=recreate, upsert=upsert)
        self.json_knowledge.load(recreate=recreate, upsert=upsert)

