"""Example usage and testing."""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.embeddings.multimodal_embedder import MultimodalEmbedder
from src.retrieval.hybrid_retriever import HybridRetriever
from src.ingestion.data_ingester import DataIngester

# Load environment
load_dotenv()


def main():
    """Run example usage."""
    
    print("=" * 60)
    print("NovaSearch - Multimodal RAG Engine")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing components...")
    embedder = MultimodalEmbedder()
    retriever = HybridRetriever(embedder)
    ingester = DataIngester()
    print("✓ Components initialized")
    
    # Create sample documents
    print("\n2. Creating sample documents...")
    sample_docs = [
        {
            "id": "doc1",
            "text": "Python is a high-level programming language known for its simplicity and readability.",
            "type": "text",
            "source": "programming.txt",
            "description": "Information about Python"
        },
        {
            "id": "doc2",
            "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
            "type": "text",
            "source": "ml.txt",
            "description": "Information about machine learning"
        },
        {
            "id": "doc3",
            "text": "Deep learning uses neural networks with multiple layers to process complex data patterns.",
            "type": "text",
            "source": "dl.txt",
            "description": "Information about deep learning"
        }
    ]
    print(f"✓ Created {len(sample_docs)} sample documents")
    
    # Index documents
    print("\n3. Indexing documents...")
    retriever.add_documents(sample_docs)
    print(f"✓ Indexed {retriever.faiss_index.ntotal} documents")
    
    # Perform searches
    print("\n4. Performing searches...")
    queries = [
        "What is Python?",
        "Tell me about machine learning",
        "Deep learning neural networks"
    ]
    
    for query in queries:
        print(f"\n   Query: {query}")
        results = retriever.search(query, k=3)
        print(f"   Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"     {i}. {result['id']} (score: {result['score']:.2f})")
            print(f"        {result['text'][:80]}...")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

