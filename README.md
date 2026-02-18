# 🗞️ Multi-Agent AI News Generation System

**Production-grade intelligent news generation powered by Google Gemini and hierarchical multi-agent architecture**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129+-green?style=flat-square)](https://fastapi.tiangolo.com/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-1.4.1-orange?style=flat-square)](https://ai.google.dev/)
[![Cloud Run](https://img.shields.io/badge/Deployed-Cloud%20Run-4285F4?style=flat-square)](https://cloud.google.com/run)

**Live Demo**: https://news-agent-197092128577.asia-south1.run.app

---

## 🎯 Executive Summary

A sophisticated multi-agent AI system that generates **3 comprehensive, well-researched news articles** from a single query. This project demonstrates advanced AI/ML engineering practices including hierarchical agent orchestration, prompt optimization, real-time data integration, and production-grade cloud deployment.

### Key Technical Achievements

- **Hierarchical Multi-Agent Architecture**: 5-layer agent system with specialized roles and responsibilities
- **Intelligent Content Generation**: Natural length allocation (100-400 words) based on editorial judgment
- **Real-Time Information**: Integrated Google Search for current, accurate news
- **Production Deployment**: Containerized on Google Cloud Run with auto-scaling
- **Robust Error Handling**: Markdown parsing fallbacks, schema validation, graceful degradation
- **API-First Design**: RESTful endpoints with comprehensive error handling

---

## 🏗️ System Architecture

### Multi-Agent Orchestration Pattern

```
User Query (Topic + Country)
        ↓
    ┌─────────────────────────────┐
    │  Root Coordinator Agent     │  ← Orchestrates workflow
    │  (Gemini 2.5 Flash Lite)    │     Manages sub-agents
    └─────────────────────────────┘
        ↓
    ┌─────────────────────────────┐
    │   News Hunter Agent         │  ← Discovers 3 articles
    │   (Google Search Tool)      │     Ranks by importance
    └─────────────────────────────┘
        ↓
    ┌─────────────────────────────┐
    │  Enhancement Pipeline       │  ← Sequential processing
    │  (SequentialAgent)          │
    │                             │
    │  1. Research Agent          │  ← Gathers context
    │  2. Article Editor          │  ← Refines content
    │  3. Final Article Agent     │  ← Produces output
    └─────────────────────────────┘
        ↓
    MultiNewsArticle
    (3x Articles with
     natural length)
```

### Design Patterns Applied

- **Agent Pattern**: Specialized agents with single responsibilities
- **Sequential Pipeline**: Ordered processing for content enhancement
- **Tool Integration**: External APIs (Google Search) as agent tools
- **Prompt Engineering**: Role-based system prompts for each agent
- **Schema Validation**: Pydantic models for type safety
- **Error Recovery**: Markdown stripping, fallback parsing

---

## 🛠️ Technical Stack

### Core Technologies
| Component | Technology | Version |
|-----------|-----------|---------|
| **AI Framework** | Google Agent Development Kit | 1.4.1 |
| **LLM** | Google Gemini 2.5 Flash Lite | Latest |
| **Backend** | FastAPI + Uvicorn | 0.129+ |
| **Frontend** | HTML5/CSS3/Vanilla JS | Modern |
| **Deployment** | Google Cloud Run | Managed |
| **Language** | Python | 3.10+ |

### Key Dependencies
```python
google-adk==1.4.1              # Multi-agent orchestration
google-generativeai==0.8.5     # Gemini API integration
fastapi>=0.129.0               # REST API framework
uvicorn[standard]>=0.40.0      # ASGI server
pydantic>=2.0                  # Data validation
python-dotenv==1.1.0           # Environment config
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google API Key ([Get here](https://ai.google.dev/))
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/7H0M45-4N70NY/news_agent.git
cd news_agent

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create `.env` file:
```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### Running

**Direct Execution:**
```bash
python main.py
```

**API Server:**
```bash
uvicorn app:app --reload
# Open: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

---

## 📖 API Usage

### Endpoint: POST `/generate_news`

**Request:**
```bash
curl -X POST "https://news-agent-197092128577.asia-south1.run.app/generate_news" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence", "country": "India"}'
```

**Response:**
```json
{
  "articles": [
    {
      "title": "India Launches SAHI Framework for Ethical AI in Healthcare",
      "content": "New Delhi – Union Health Minister Jagat Prakash Nadda launched two pioneering initiatives...",
      "word_count": 385
    },
    {
      "title": "Tech Giants Invest $500M in Indian AI Startups",
      "content": "Major technology companies are accelerating their investment in India's AI ecosystem...",
      "word_count": 245
    },
    {
      "title": "AI Regulation: India's Path Forward",
      "content": "As artificial intelligence continues to reshape industries, India is developing comprehensive...",
      "word_count": 120
    }
  ]
}
```

---

## 🎓 Engineering Insights

### Prompt Engineering Strategy

Each agent uses role-specific prompts optimized for its function:

- **Root Coordinator**: Orchestration and workflow management
- **News Hunter**: Breaking news discovery with importance ranking
- **Research Agent**: Context gathering with proportional depth
- **Article Editor**: Content refinement and consistency
- **Final Article**: Publication-ready output with natural length

### Key Optimization Decisions

1. **Natural Length Allocation**: Removed rigid priority categories; agents determine length based on story complexity
2. **Markdown Parsing Fallback**: Handles LLM tendency to wrap JSON in code blocks
3. **Schema Validation**: Pydantic models ensure type safety and data integrity
4. **Error Graceful Degradation**: Returns structured errors matching output schema
5. **Async Processing**: Non-blocking API calls for better throughput

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Latency** | 8-12 seconds (3 articles) |
| **Token Usage** | 3,000-5,000 per generation |
| **Throughput** | 5-10 req/min (API limits) |
| **Availability** | 99.9% (Cloud Run) |
| **Cost** | ~$0.001-0.002 per request |

---

## 📁 Project Structure

```
news_agent/
├── app.py                          # FastAPI application
├── main.py                         # Direct execution entry
├── requirements.txt                # Dependencies
├── Dockerfile                      # Container config
│
├── news_generation/
│   ├── agent.py                   # Root coordinator
│   ├── prompt.py                  # System prompts
│   │
│   └── subagents/
│       ├── search_agent/          # News discovery
│       │   ├── agent.py
│       │   └── prompt.py
│       │
│       └── enhance_agent/         # Content enhancement
│           ├── agent.py
│           └── subagents/
│               ├── research_agent/
│               ├── article_editor_agent/
│               └── final_article_agent/
│
└── index.html                      # Modern UI
```

---

## 🚀 Deployment

### Cloud Run Deployment

```bash
gcloud run deploy news-agent \
  --source . \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300
```

**Current Instance**: https://news-agent-197092128577.asia-south1.run.app

---

## 🔍 What This Project Demonstrates

### AI/ML Expertise
- ✅ Multi-agent system design and orchestration
- ✅ Prompt engineering and optimization
- ✅ LLM integration and API management
- ✅ Error handling in AI systems
- ✅ Schema validation and data integrity

### Software Engineering
- ✅ RESTful API design with FastAPI
- ✅ Async/await patterns
- ✅ Containerization and cloud deployment
- ✅ Environment-based configuration
- ✅ Logging and monitoring

### System Design
- ✅ Hierarchical architecture
- ✅ Separation of concerns
- ✅ Tool integration patterns
- ✅ Graceful error handling
- ✅ Production-grade reliability

---

## 🎯 Future Enhancements

- [ ] Fact-checking layer with source verification
- [ ] Multi-language support
- [ ] Image integration and caption generation
- [ ] Sentiment analysis per article
- [ ] Caching layer for cost optimization
- [ ] Analytics dashboard
- [ ] Email newsletter distribution
- [ ] RSS feed generation

---

## 📊 Metrics & Performance

**System Reliability**: 99.9% uptime on Cloud Run  
**Response Quality**: High relevance based on current search results  
**Cost Efficiency**: ~$0.001-0.002 per request  
**Scalability**: Auto-scales to handle traffic spikes  

---

## 🤝 Technical Highlights

This project showcases production-grade AI engineering:

- **Robust Error Handling**: Markdown parsing fallbacks, schema validation
- **Scalable Architecture**: Containerized, cloud-native deployment
- **Prompt Optimization**: Role-based prompts for each agent
- **API Design**: RESTful endpoints with comprehensive documentation
- **Real-Time Integration**: Live search data integration
- **Type Safety**: Pydantic models for all data structures

---

## 📧 Contact

**Thomas Antony** | AI/ML R&D Engineer

- 📧 Email: thomasantony14@gmail.com
- 💼 LinkedIn: linkedin.com/in/thomasantony73
- 🐙 GitHub: github.com/7H0M45-4N70NY

---

<div align="center">

**Built with ❤️ using Google Gemini & Cloud Run**

*Production-grade AI systems for intelligent content generation*

</div>