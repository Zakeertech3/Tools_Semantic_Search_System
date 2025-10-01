# Tool Semantic Search System

A FastAPI-based semantic search system that enables intelligent discovery of development tools using vector embeddings and natural language queries.

## Problem Statement

Traditional keyword-based search systems fail to understand the semantic meaning and context behind user queries. When developers search for tools, they often need to know exact keywords or tool names, making discovery difficult. This project solves this problem by implementing semantic search that understands the intent and context of queries, returning relevant tools even when exact keywords don't match.

**Key Challenges Addressed:**
- Finding tools based on conceptual similarity rather than exact keyword matches
- Enabling natural language queries for tool discovery
- Maintaining fast search performance across large datasets
- Tracking search patterns and interaction history

## Solution Architecture

### System Overview

```
┌─────────────────┐
│   Streamlit UI  │
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────┐
│   FastAPI       │
│   (Backend)     │
└────┬────────┬───┘
     │        │
     │        │
     ▼        ▼
┌─────────┐ ┌──────────────┐
│PostgreSQL│ │   Qdrant     │
│(Metadata)│ │(Vector Store)│
└──────────┘ └──────────────┘
```

### Data Flow

1. **Insert Tool**: User submits tool details → FastAPI generates embeddings → Stores in both PostgreSQL (metadata) and Qdrant (vectors)
2. **Search**: User query → Convert to embeddings → Qdrant similarity search → Retrieve metadata from PostgreSQL → Return ranked results
3. **History Tracking**: All searches logged in PostgreSQL with timestamps and response times

## Tech Stack

**Backend:**
- FastAPI - REST API framework
- Python 3.9+ - Core language
- SQLAlchemy - PostgreSQL ORM
- Sentence Transformers - Embedding generation
- all-mpnet-base-v2 - Embedding model (768-dimensional vectors)

**Databases (Dockerized):**
- PostgreSQL 15 - Structured data storage (runs in Docker container)
- Qdrant - Vector database for semantic search (runs in Docker container)

**Frontend:**
- Streamlit - Interactive web interface

**Infrastructure:**
- Docker & Docker Compose - Containerization
- Uvicorn - ASGI server

## Project Structure

```
tool-semantic-search/
├── app/
│   ├── api/routes/          # API endpoints
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business Logic
│   ├── database/            # Database connections
│   └── config/              # Configuration
├── streamlit_app/           # Frontend application
├── docker/                  # Docker configuration
│   ├── docker-compose.yml
│   └── postgres/init.sql
├── tests/                   # Test cases
├── sync_tools.py           # Tool synchronization script
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Docker Desktop installed and running
- Git

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Then edit `.env` file with your specific configuration:

```env
POSTGRES_DB=tool_search_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=tools_collection

EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
VECTOR_SIZE=768

API_HOST=0.0.0.0
API_PORT=8000
```

### Step 5: Start Docker Containers (PostgreSQL & Qdrant)

```bash
cd docker
docker compose up -d
```

This will start:
- **PostgreSQL 15** container on port 5432
- **Qdrant** vector database container on port 6333
- **pgAdmin** (optional) on port 8080

Wait 30 seconds for database initialization.

### Step 6: Sync Pre-loaded Tools

```bash
cd ..
python sync_tools.py
```

This will sync 35 pre-loaded tools to both databases.

### Step 7: Start FastAPI Backend

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Step 8: Start Streamlit Frontend

Open a new terminal:

```bash
streamlit run streamlit_app/app.py
```

Frontend will open automatically in your browser (typically http://localhost:8501)

## Verify Installation

### Check PostgreSQL Data

```bash
python -c "from app.database.postgres import SessionLocal; from app.models.tool import Tool; db = SessionLocal(); print(f'Tools in PostgreSQL: {db.query(Tool).count()}'); db.close()"
```

Expected output: `Tools in PostgreSQL: 35`

### Check Qdrant Vectors

```bash
python -c "from app.services.qdrant_service import qdrant_service; info = qdrant_service.client.get_collection(qdrant_service.collection_name); print(f'Vectors in Qdrant: {info.points_count}')"
```

Expected output: `Vectors in Qdrant: 35`

## Usage

### Search for Tools

Navigate to the "Search Tools" tab and enter natural language queries:

- "machine learning framework"
- "database for caching"
- "containerization tools"
- "frontend javascript library"

Results are ranked by semantic similarity (0.0 to 1.0 score).

### Add New Tools

Navigate to the "Add Tool" tab:
1. Enter tool name
2. Add description
3. Provide comma-separated tags
4. Add metadata in JSON format
5. Click "Add Tool"

The tool will be automatically embedded and indexed.

### Manage Tools

Navigate to "Manage Tools" tab to:
- View all tools
- Delete existing tools
- Check tool details and metadata

## API Endpoints

### Tools
- `POST /tools/` - Create new tool
- `GET /tools/` - List all tools
- `GET /tools/{id}` - Get specific tool
- `PUT /tools/{id}` - Update tool
- `DELETE /tools/{id}` - Delete tool

### Search
- `POST /search/` - Semantic search
  - Body: `{"query": "your search query", "limit": 5}`
  - Returns: Ranked results with similarity scores

### Health
- `GET /` - API status
- `GET /health` - Health check

## Testing

Run test suite:

```bash
pytest tests/
```

## Troubleshooting

### Docker containers not starting
```bash
docker compose down -v
docker compose up -d
```

### Embeddings not syncing
```bash
python sync_tools.py
```

### Port already in use
Change ports in `.env` file and restart services.

### Connection refused errors
Ensure Docker containers are running:
```bash
docker ps
```

## Key Features

- Semantic search using state-of-the-art embeddings
- Dual database architecture (SQL + Vector)
- Search history tracking with timestamps
- Real-time tool insertion and indexing
- RESTful API with automatic documentation
- Interactive web interface
- Docker containerization for easy deployment

## Performance

- Average search response time: 50-150ms
- Embedding generation: ~100ms per tool
- Supports 1000+ tools efficiently
- Cosine similarity for vector matching

## Future Enhancements

- User authentication and authorization
- Advanced filtering options
- Batch tool import via CSV
- Search analytics dashboard
- API rate limiting
- Caching layer for frequent queries

## License

MIT

## Acknowledgments

- Sentence Transformers for embedding models
- Qdrant for vector database
- FastAPI framework
- Streamlit for rapid UI development