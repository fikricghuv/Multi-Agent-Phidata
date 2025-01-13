from phi.model.openai import OpenAIChat
from phi.embedder.openai import OpenAIEmbedder

model_openai = OpenAIChat(id="gpt-4o-2024-11-20", max_tokens=1024, temperature=0.3)
model_embedd_openai = OpenAIEmbedder(model="text-embedding-3-small")
# model_groq = Groq(id="llama3-groq-70b-8192-tool-use-preview")
# model_ollama = Ollama(id="llama3.2")
# model_ollama_embeddings = OllamaEmbedder()
