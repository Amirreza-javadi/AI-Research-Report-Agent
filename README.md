# 🔎 AI Research & Report Agent

### An Adaptive AI Research System That Searches, Evaluates, and Generates Structured Reports

An AI-powered research backend designed to investigate complex topics through an adaptive research workflow.

Instead of simply generating an answer from a single prompt, the system plans research questions, searches the web, evaluates information coverage, identifies knowledge gaps, and iteratively gathers additional information before generating a structured Markdown report.

Built with **Python, FastAPI, LangGraph, Groq, Tavily, SQLAlchemy 2.0, and MySQL**, this project explores how to engineer AI applications that combine LLMs, external tools, stateful workflows, and persistent storage.

> **Project focus:** AI Engineering · Agentic Workflows · Adaptive Research · LLM Integration · Backend Development

---

## ✨ Why This Project?

Traditional LLM applications often follow a simple pattern:

`User Input → LLM → Response`

But complex research tasks require more than a single generation step.

An effective research system needs to determine what to investigate, collect relevant information, evaluate whether the findings are sufficient, and decide what to investigate next.

This project implements an adaptive workflow that separates these responsibilities into specialized nodes coordinated by LangGraph.

### Key capabilities

- 🧠 **Structured Research Planning** — Generates research questions and search queries from a user's request.
- 🌐 **Web Search Integration** — Retrieves relevant web results through Tavily.
- 🔄 **Adaptive Research Loop** — Evaluates research coverage and performs additional searches when necessary.
- 📊 **Coverage Evaluation** — Assesses collected findings and identifies potential knowledge gaps.
- 📝 **Automated Report Generation** — Produces structured Markdown reports from collected research.
- ⚙️ **API-First Architecture** — Exposes research functionality through a FastAPI backend.
- 🗄️ **Persistent Storage** — Uses SQLAlchemy 2.0 and MySQL to store research requests and results.
- 🧪 **Automated Testing** — Includes tests for workflow components, graph execution, and API behavior.

---

## 🏗️ System Architecture

The research workflow is organized into specialized nodes connected through LangGraph.

```mermaid
flowchart TD
    A[Research Request] --> B[Research Planner]
    B --> C[Web Researcher]
    C --> D[Research Evaluator]
    D --> E{Coverage Sufficient?}
    E -->|No, More Research Needed| C
    E -->|Yes| F[Report Writer]
    E -->|Iteration Limit Reached| F
    E -->|No Additional Queries| F
    F --> G[Markdown Report]
```

### Workflow overview

**1. Research Planner**

Analyzes the requested topic and produces structured research questions and search queries.

**2. Web Researcher**

Uses Tavily to retrieve relevant web results and collects source information while avoiding duplicate URLs.

**3. Research Evaluator**

Evaluates the available research, assigns a coverage score, provides feedback, and proposes additional queries when needed.

**4. Adaptive Routing**

LangGraph determines whether the workflow should continue researching or proceed to report generation based on the coverage score, remaining iterations, and availability of additional queries.

**5. Report Writer**

Uses the collected findings to generate a Markdown research report.

**6. API and Persistence Layer**

FastAPI exposes the research endpoints, while SQLAlchemy and MySQL manage research records and their results.

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core application language |
| FastAPI | REST API development |
| LangGraph | Stateful, multi-step AI workflow orchestration |
| Groq | LLM inference |
| Tavily | Web search for AI applications |
| Pydantic | Data validation and structured data models |
| Pydantic Settings | Environment-based configuration |
| SQLAlchemy 2.0 | Database access and ORM |
| MySQL | Persistent storage |
| Pytest | Automated testing |
| Uvicorn | ASGI application server |

---

## 📂 Project Structure

```text
app/
├──ai/
│   ├── nodes/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── evaluator.py
│   │   └── report_writer.py
│   ├── tools/
│   │   └── web_searche.py
│   ├── state.py
│   └── graph.py
├── api/
│   └── v1/
├── core/
│   └── config.py
├── db/
├── models/
├── schemas/
├── services/
├── main.py
└── ...

tests/
├── test_graph_routing.py
├── test_researcher.py
├── test_evaluator.py
├── test_report_writer.py
├── test_graph_integration.py
└── test_research_api.py
```

*The tree highlights the main components; additional files may exist in the repository.*

---

## 🚀 Getting Started

### Prerequisites

Before running the application, make sure you have:

- Python 3.11 or newer
- MySQL
- A Groq API key
- A Tavily API key
- Network access to the configured external services

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your repository URL and project directory.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure the required values.

Example:

```env
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/ai_research_agent

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Use the exact variable names expected by your project's configuration.

**Security notes:**

- Never commit `.env` to Git.
- Never expose API keys in source code, screenshots, logs, or public repositories.
- Keep `.env.example` limited to placeholder values.

### 5. Create the MySQL database

Connect to MySQL and execute:

```sql
CREATE DATABASE ai_research_agent
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Ensure the database credentials in `.env` match your local configuration.

### 6. Start the API server

```bash
python -m uvicorn app.main:app --reload
```

The application should now be available at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Swagger UI can be used to explore and test the available API endpoints.

---

## 🔌 API Endpoints

The backend exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check API availability |
| `POST` | `/api/v1/research` | Create a research request and execute the research workflow |
| `GET` | `/api/v1/research` | Retrieve research records with pagination |
| `GET` | `/api/v1/research/{research_id}` | Retrieve a specific research record |

### Example: Create a Research Request

**Request**

```http
POST /api/v1/research
Content-Type: application/json
```

```json
{
  "topic": "The impact of AI agents on software development",
  "audience": "Software developers",
  "depth": "deep"
}
```

The request fields must match the validation rules defined by the API schemas.

When execution succeeds, the response includes the research record, generated report, and collected sources.

Example response shape:

```json
{
  "id": 1,
  "topic": "The impact of AI agents on software development",
  "audience": "Software developers",
  "depth": "deep",
  "status": "completed",
  "report_markdown": "# Research Report\n\n...",
  "sources": [
    {
      "title": "Example Source",
      "url": "https://example.com/article"
    }
  ],
  "error_message": null,
  "created_at": "2026-01-01T12:00:00",
  "updated_at": "2026-01-01T12:01:00"
}
```

*This is an illustrative response, not a captured live API response. Actual output depends on the configured services and implementation.*

### Pagination

The research list endpoint supports pagination through `limit` and `offset`.

Example:

```http
GET /api/v1/research?limit=10&offset=0
```

---

## 🧪 Testing

Automated tests help validate workflow behavior, graph routing, report generation, and API functionality.

Run the complete test suite:

```bash
python -m pytest
```

Run a specific test module:

```bash
python -m pytest tests/test_graph_integration.py -v
```

### External service isolation

Tests that exercise API behavior can mock the research graph to avoid unnecessary external API calls.

This makes those tests suitable for environments where access to Groq or Tavily is unavailable.

**Important:** Passing mocked tests validates the behaviors covered by those tests. It does not independently verify live web search, real LLM responses, or the complete production execution path.

---

## 🔐 Configuration and Reliability

The application depends on external services for LLM inference and web search.

For a successful live research run, configure valid credentials and ensure that the services are reachable from your environment.

A production deployment would also benefit from:

- More granular external API error reporting
- Retry policies and timeouts
- Rate-limit handling
- Background execution for long-running research jobs
- Persistent job status updates
- Observability and structured logging

These are important considerations when evolving an AI prototype into a production service.

---

## 🛣️ Roadmap

Potential next improvements include:

- [ ] Add background execution for long-running research jobs.
- [ ] Improve retries and error handling for external services.
- [ ] Add authentication and authorization.
- [ ] Introduce research history filters and sorting.
- [ ] Add richer source attribution and report metadata.
- [ ] Expand evaluation metrics and automated workflow tests.
- [ ] Add Docker support for reproducible deployment.
- [ ] Add CI checks for tests and code quality.
- [ ] Build a frontend for interactive research and report viewing.

---

## 💡 Engineering Principles

This project explores several important AI engineering concepts:

- **Workflow orchestration:** Separating research into explicit, testable stages.
- **Structured LLM outputs:** Using typed data models to constrain model responses.
- **Tool integration:** Connecting language models to external web search.
- **Adaptive execution:** Using evaluation results to guide subsequent actions.
- **State management:** Passing research context between workflow nodes.
- **Separation of concerns:** Keeping AI logic, API routes, persistence, and configuration in distinct modules.
- **Testability:** Using mocks to test application behavior independently of external service availability.

---

## 👨‍💻 About This Project

I built this project to deepen my understanding of AI Engineering and the development of tool-using, stateful AI systems.

My focus is on moving beyond simple LLM calls toward applications that combine structured planning, external tools, iterative evaluation, workflow orchestration, and backend engineering.

I'm continuously improving my skills by building practical projects and sharing what I learn.

**Interested in AI Engineering, LLM applications, or backend development? Let's connect.**

---

## 📄 License

Choose and add an appropriate open-source license before distributing this project.