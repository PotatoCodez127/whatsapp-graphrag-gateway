# 🌐 WhatsApp ↔ GraphRAG Webhook Edge Gateway

An enterprise-grade, asynchronous webhook gateway microservice designed to bridge the Meta WhatsApp Cloud API with a centralized GraphRAG-powered AI backend engine. Built using Flask, Gunicorn, and multi-threaded processing pools to handle high-throughput message routing under strict server response deadlines.

## ⚡ Key Architectural Features

### 1. Asynchronous Acknowledgment Deadlines
Meta's WhatsApp Cloud API requires webhook targets to respond with an HTTP `200 OK` status code within standard sub-second window parameters to prevent event retry loops. 
- **The Solution:** This gateway instantly detaches incoming network payloads into an isolated background worker thread (`threading.Thread`) to manage the underlying GraphRAG API inference requests and text deliveries. 
- **The Result:** The main request routing handler returns an immediate `200 OK` acknowledgment back to Meta's edge nodes, eliminating duplicate webhook event deliveries and server load spikes.

### 2. Isolated Token Handshaking & Security
Features built-in endpoint verification logic that automatically intercepts and parses Meta's explicit setup sequences (`hub.mode`, `hub.challenge`, and `hub.verify_token`), protecting your internal downstream AI nodes from unauthorized query spoofing or scanning attempts.

### 3. Lean Microservice Footprint
Optimized down to a minimalist production footprint. All unneeded dependency bloat (such as development async routers) has been pruned, moving execution to **Gunicorn**—the industry-standard, multi-worker Unix WSGI server.

## 🛠️ Tech Stack
- **Core Engine:** Python, Flask
- **Networking Layer:** Requests, Gunicorn
- **Quality Assurance:** Pytest, Black, Ruff
- **Infrastructure:** Docker, GitHub Actions Continuous Integration

## 🧹 Code Quality & Standards
Development pipelines and validation styles are configured centrally via the root `pyproject.toml` hub:
- **Black:** Governs PEP 8 whitespace layout stability and consistency across modules.
- **Ruff:** Executes static syntax compilation audits, structural error monitoring, and enforces explicit first-party Isort import sorting constraints.

To check and format code locally:
```bash
python -m black .
python -m ruff check . --fix
```

## ⚙️ Setup & Deployment Guide

### Option A: Local Enterprise Installation
1. Clone the repository and install the production-grade dependency sheet:
```bash
git clone [https://github.com/PotatoCodez127/whatsapp-graphrag-gateway.git](https://github.com/PotatoCodez127/whatsapp-graphrag-gateway.git)
cd whatsapp-graphrag-gateway
pip install -r requirements.txt
```

2. Configure environmental variables by creating a secure .env file at the root:
```bash
WHATSAPP_TOKEN=your_meta_access_token
PHONE_NUMBER_ID=your_whatsapp_phone_number_id
VERIFY_TOKEN=your_custom_secure_handshake_verify_token
CHATBOT_API_URL=[https://your-central-graphrag-api.com/chat](https://your-central-graphrag-api.com/chat)
API_SECRET_KEY=your_secure_downstream_brain_api_key
```

3. Run the local verification unit tests to confirm router handler integrity:
```bash
python -m pytest
```

### Option B: Containerized Production Isolation (Recommended)
This service includes a production-grade multi-threaded container blueprint to completely remove local system dependency drift.

1. Build the lean, isolated Linux-slim runtime image:
```bash
docker build -t whatsapp-graphrag-gateway .
```

2. Fire up the application container, binding Gunicorn workers natively to production port 5001:
```bash
docker run -d -p 5001:5001 --env-file .env --name gateway-instance whatsapp-graphrag-gateway
```

## 🤖 Continuous Integration (CI/CD)
Automated testing and code validation gates are executed natively via GitHub Actions (.github/workflows/ci.yml). Every single commit or merge pull request opened against tracking branches spins up an isolated Ubuntu build node that triggers comprehensive dependency resolution, strict Black visual compliance checks, Ruff compilation audits, and runs your pytest suite to guarantee absolute gateway routing health before deployment.

---