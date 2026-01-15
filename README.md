# LedgerMind – Data-Grounded Financial Chatbot

LedgerMind is a production-ready financial chatbot built to answer questions strictly from structured datasets (trades and holdings). The system is designed to be deterministic, explainable, and safe against hallucination, making it suitable for real-world financial data use cases.

This project was built as part of an AI/ML technical task and intentionally delivered at production quality rather than prototype level.

---

## Key Principles

- Answers are generated **only** from the provided datasets  
- No external internet access or pretrained knowledge leakage  
- Deterministic logic instead of probabilistic guessing  
- Explicit refusal for unsupported, ambiguous, predictive, or explanatory questions  
- Clear separation of concerns between intent detection and execution  

---

## What the Chatbot Can Do

The chatbot supports the following categories of questions:

### 1. Counting
- Total number of trades
- Total number of holdings

Examples:
- "How many trades are there?"
- "Number of holdings available"

---

### 2. Aggregations (SUM, MEAN)

Supported metrics are inferred from the question and dataset context.

Trades dataset:
- TotalCash
- Quantity
- Price (average)

Holdings dataset:
- MV_Base (market value)
- Price (average)

Examples:
- "Total trades value"
- "Average trade price"
- "Total holdings value"
- "Average holding price"

---

### 3. Performance Comparison

The chatbot can identify the best performing fund based on yearly profit and loss.

- Metric used: PL_YTD
- Dataset: holdings
- Grouping: PortfolioName

Examples:
- "Which fund performed the best based on yearly P&L?"
- "Show the top performing fund"
- "Which fund has the highest yearly profit and loss?"

---

### 4. Safe Refusals (By Design)

The chatbot explicitly refuses to answer when:
- The answer is not present in the dataset
- The question is predictive or speculative
- The question asks for explanations or reasoning
- The question combines multiple intents
- The question is ambiguous or underspecified

Example refusals:
- "What will be the best fund next year?"
- "Explain why this fund performed better"
- "Average price and how many trades exist"

Response:
Sorry can not find the answer


This behavior is intentional and critical for trustworthiness.

---

## System Architecture

The system is divided into three clean layers:

### 1. Intent Parsing Layer
- Converts natural language into a structured intent
- Determines:
  - Intent type (COUNT, AGGREGATION, PERFORMANCE, UNKNOWN)
  - Dataset (trades or holdings)
  - Aggregation type (SUM or MEAN)
- Explicitly blocks:
  - Compound questions
  - Explanation queries
  - Unsupported phrasing

### 2. Execution Layer
- Executes deterministic Pandas operations
- No LLM involvement in calculations
- Column selection is rule-based and transparent
- Produces exact numeric answers or explicit refusal

### 3. Presentation Layer
- Clean conversational UI
- Frontend never computes or infers answers
- Backend is the single source of truth

---

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- Pandas
- Docker
- Deployed on Hugging Face Spaces (Docker runtime)

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Deployed on Vercel

---

## Deployment

### Backend (Hugging Face Spaces)

- Docker-based FastAPI deployment
- Public HTTPS endpoint
- Port 7860 (Hugging Face standard)
- Health endpoint available at `/health`

Backend URL:
https://shahirun-ledgermind-backend.hf.space


---

### Frontend (Vercel)

- Production build using environment variables
- Backend URL injected via:

NEXT_PUBLIC_API_BASE_URL


Frontend URL:
https://ledgermind-1tvnlrdn8-shahiruns-projects.vercel.app/


---

## Running Locally

### Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend will run at:
http://127.0.0.1:8000/


---

### Frontend

cd frontend
npm install
npm run dev

Create a `.env.local` file:
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000


---

## Testing Philosophy

The chatbot was tested against:
- Valid queries with correct answers
- Edge-case phrasing
- Ambiguous and compound questions
- Out-of-scope and predictive questions

The system prefers **refusal over incorrect answers**, which is a deliberate design choice for financial correctness.

---

## Design Decisions

- No LLM used for reasoning or calculations to avoid hallucination
- Rule-based intent parsing for full control and auditability
- Dockerized backend for reproducibility
- Public deployment to demonstrate real production readiness

---

## Future Improvements

- Vector-based semantic column mapping
- Multi-intent query decomposition
- Role-based access control
- Query plan visualization
- Dataset schema introspection API

---

## Author

Shahirun

This project reflects an emphasis on correctness, safety, and production-level engineering practices rather than rapid prototyping.
