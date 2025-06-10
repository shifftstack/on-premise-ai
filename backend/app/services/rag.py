from langchain.embeddings import OllamaEmbeddings
import chromadb

CHROMA_COLLECTION = "documents"
CHROMA_PATH = "chromadb_store"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)
ollama_embeddings = OllamaEmbeddings(model="llama4")


def retrieve_context(query, k=4):
    query_embedding = ollama_embeddings.embed_query(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    contexts = [doc for doc in results["documents"][0]]
    metadatas = results["metadatas"][0]
    return contexts, metadatas 