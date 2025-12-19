## 🔁 End-to-End Workflow

The system is built as a production-style pipeline with two main stages:

1. **Indexing & Ingestion Pipeline**
2. **Query & Retrieval-Augmented Generation (RAG) Pipeline**

---

### 1️⃣ Indexing & Ingestion Pipeline

1. **Data collection**
   - Ingest raw text documents (PDFs, articles, docs) and image metadata from files, APIs, or other data sources.
   - Publish every new document or image as an event to Apache Kafka topics (e.g., `raw-documents`, `raw-images`) for downstream processing.

2. **Real-time preprocessing (Kafka → Spark)**
   - Apache Spark Streaming consumes events from Kafka in mini-batches.
   - Cleans and normalizes text (tokenization, lowercasing, boilerplate removal) and extracts structured metadata such as titles, tags, and timestamps.

3. **Multi-modal embedding generation**
   - **Text:** Use OpenAI text embeddings (e.g., `text-embedding-3-large`) to convert document chunks into dense vectors.
   - **Images:** Use CLIP or a similar vision model to generate embeddings from image content or URLs.
   - Maintain a consistent vector space for both text and image embeddings to enable true multi-modal similarity search.

4. **Vector indexing & storage**
   - Store embeddings in:
     - **FAISS** for ultra-fast approximate nearest-neighbor search at scale.
     - **Elasticsearch** with `dense_vector` / k-NN for vector search combined with rich filtering and metadata queries.
   - Persist original content and metadata for accurate grounding and user-facing display.

5. **Index lifecycle & optimization**
   - Periodically rebuild or compact FAISS indices to keep search fast and memory-efficient.
   - Use Elasticsearch index lifecycle policies for automatic scaling, rollover, and retention of historical data.

---

### 2️⃣ Query & RAG Pipeline

1. **Query intake**
   - Users send natural-language queries (optionally with an image) via a REST API or web UI.
   - The backend normalizes, validates, and logs each request for monitoring and analytics.

2. **Multi-modal query embedding**
   - Embed the text query using the same OpenAI embedding model used during indexing.
   - If an image is provided, compute its CLIP embedding and fuse it with the text embedding (e.g., weighted sum or concatenation) for richer intent understanding.

3. **Hybrid retrieval (FAISS + Elasticsearch)**
   - Use **FAISS** to perform high-speed semantic similarity search over the global embedding space.
   - Use **Elasticsearch** k-NN search to apply filters (time, tag, document type) and metadata-aware ranking.
   - Merge, rank, and deduplicate candidates into a final context set for the LLM.

4. **RAG orchestration with LangChain**
   - LangChain builds a RAG pipeline that:
     - Feeds the user question and top‑k retrieved context chunks (text + image captions/metadata) into a prompt.
     - Calls the LLM (OpenAI Chat model) with this grounded context to avoid hallucinations.

5. **LLM answer generation**
   - The LLM generates a concise, context-aware answer that is explicitly grounded in the retrieved documents and images.
   - Multi-modal responses can reference relevant images (IDs/URLs), which the UI displays alongside the generated text.

6. **Response delivery & observability**
   - The API returns:
     - The final answer.
     - The top‑k supporting documents/images with metadata and similarity scores.
   - Log query, latency, retrieval metrics, and user feedback to continuously tune retrieval and generation quality.

---

### ⚙️ Optional Enhancements

- **Intelligent re-ranking:** Add a cross-encoder or LLM-based re-ranker on top of FAISS/Elasticsearch results to further boost relevance.
- **Feedback-driven learning:** Use thumbs up/down and click-through behavior to adapt ranking over time.
- **Monitoring & quality metrics:** Track Precision@k, MRR, latency, and error rates in dashboards (Prometheus/Grafana, Kibana) for production-grade observability.
