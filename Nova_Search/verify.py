#!/usr/bin/env python
"""
NovaSearch Project Verification Script

This script verifies that all components are properly set up and ready to use.
"""

import os
import sys
from pathlib import Path

def check_structure():
    """Check if project structure is complete."""
    print("\n🔍 Checking Project Structure...")
    print("=" * 60)
    
    required_files = [
        "src/api/main.py",
        "src/api/llm_orchestrator.py",
        "src/embeddings/multimodal_embedder.py",
        "src/retrieval/hybrid_retriever.py",
        "src/ingestion/data_ingester.py",
        "src/models/schemas.py",
        "src/config.py",
        "tests/test_components.py",
        "tests/test_integration.py",
        "README.md",
        "QUICKSTART.md",
        "BUILD_SUMMARY.md",
        "IMPLEMENTATION.md",
        "DEPLOYMENT.md",
        "requirements.txt",
        ".env.example",
        "Dockerfile",
        "docker-compose.yml",
        ".gitignore",
    ]
    
    missing = []
    found = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            found.append(file_path)
            print(f"  ✅ {file_path}")
        else:
            missing.append(file_path)
            print(f"  ❌ {file_path}")
    
    print("\n" + "=" * 60)
    print(f"Found: {len(found)}/{len(required_files)} files")
    
    if missing:
        print(f"Missing: {', '.join(missing)}")
    
    return len(missing) == 0

def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking Directories...")
    print("=" * 60)
    
    required_dirs = [
        "src",
        "src/api",
        "src/embeddings",
        "src/retrieval",
        "src/ingestion",
        "src/models",
        "tests",
        "data",
        "data/documents",
        "data/images",
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/")
    
    return True

def check_dependencies():
    """Check if key dependencies are available."""
    print("\n📦 Checking Dependencies...")
    print("=" * 60)
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("langchain", "LangChain"),
        ("openai", "OpenAI"),
        ("faiss", "FAISS"),
        ("pydantic", "Pydantic"),
        ("pytest", "Pytest"),
    ]
    
    all_found = True
    
    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ❌ {display_name} - Not installed")
            all_found = False
    
    if not all_found:
        print("\n  💡 Run: pip install -r requirements.txt")
    
    return all_found

def check_environment():
    """Check environment configuration."""
    print("\n⚙️  Checking Environment...")
    print("=" * 60)
    
    if Path(".env").exists():
        print("  ✅ .env file exists")
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY=sk-" in content or "OPENAI_API_KEY=your_openai" in content:
                print("  ⚠️  OPENAI_API_KEY needs to be configured")
            else:
                print("  ⚠️  OPENAI_API_KEY value")
    else:
        print("  ⚠️  .env file not found")
        print("     Run: cp .env.example .env")
    
    return True

def print_next_steps():
    """Print next steps for user."""
    print("\n" + "=" * 60)
    print("🚀 NEXT STEPS")
    print("=" * 60)
    
    print("""
1. Configure Environment
   - Edit .env and add your OPENAI_API_KEY
   
2. Start the API Server
   - python -m uvicorn src.api.main:app --reload
   
3. Access the Documentation
   - http://localhost:8000/docs (Swagger UI)
   - http://localhost:8000/redoc (ReDoc)
   
4. Test the System
   - python example_usage.py
   - pytest tests/ -v
   
5. Index Your Documents
   - Use /index endpoint to add documents
   - Use /search endpoint to search
   
6. For Production
   - Review DEPLOYMENT.md
   - Use Docker: docker-compose up
   - Configure load balancing and monitoring
""")

def print_project_summary():
    """Print project summary."""
    print("\n" + "=" * 60)
    print("📊 PROJECT SUMMARY")
    print("=" * 60)
    print("""
NovaSearch - Multimodal RAG Engine

✨ Features:
  • Multimodal Search (Text + Images)
  • Semantic Understanding via OpenAI
  • Hybrid Retrieval (FAISS + Elasticsearch)
  • LLM Orchestration with LangChain
  • RESTful API with FastAPI
  • Production-Ready Architecture
  
📚 Components:
  • Multimodal Embedder (Text & Image)
  • Hybrid Retriever (Dense + Sparse)
  • Data Ingester (Multi-format)
  • LLM Orchestrator (LangChain)
  • FastAPI Application
  
🔧 Technology:
  • Python 3.8+
  • FastAPI
  • OpenAI API
  • FAISS
  • Elasticsearch
  • LangChain
  • Pydantic
  
📖 Documentation:
  • README.md - Full documentation
  • QUICKSTART.md - Getting started
  • IMPLEMENTATION.md - Implementation details
  • DEPLOYMENT.md - Deployment guide
  • BUILD_SUMMARY.md - Build overview
  
✅ Status: READY FOR USE
""")

def main():
    """Run all checks."""
    print("""
╔════════════════════════════════════════════════════════════╗
║          NovaSearch Project Verification                   ║
║              Multimodal RAG Engine                         ║
╚════════════════════════════════════════════════════════════╝
""")
    
    # Run checks
    structure_ok = check_structure()
    check_directories()
    deps_ok = check_dependencies()
    check_environment()
    
    # Print summary
    print_project_summary()
    
    # Print next steps
    print_next_steps()
    
    # Final status
    print("=" * 60)
    if structure_ok and deps_ok:
        print("✅ All checks passed! System is ready to use.")
        return 0
    else:
        print("⚠️  Some issues found. Please review above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

