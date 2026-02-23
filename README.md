# WhatsApp ↔ GraphRAG Webhook Gateway

This repository contains a dedicated webhook server designed to connect the Meta WhatsApp Cloud API to a GraphRAG-powered AI backend. It securely receives incoming WhatsApp messages, parses the payload, and forwards the queries to your core AI Agent API for processing.

## 🚀 Features
- **Secure Webhook Verification**: Automatically handles Meta's `hub.challenge` verification process.
- **Message Routing**: Parses incoming WhatsApp payloads and extracts the text, sender number, and timestamp.
- **GraphRAG Integration**: Acts as a lightweight middleman to pass messages to your central GraphRAG API (e.g., `zappies-central-api`).
- **Async Ready**: Designed to quickly acknowledge receipt to Meta (preventing timeouts) while processing the AI response asynchronously.

## 🛠️ Prerequisites

1. Python 3.8+
2. A Meta Developer Account with a configured WhatsApp Business App.
3. Your core GraphRAG API running (the main bot template).
4. ngrok (https://ngrok.com/download) (for exposing the local webhook to the internet).

## ⚙️ Setup Instructions

### Step 1: Install Dependencies
Open your terminal in the project directory and install the required packages:

pip install -r requirements.txt


### Step 2: Configure Environment Variables
Create a `.env` file in the root directory and add your credentials:

# Meta WhatsApp Credentials
WHATSAPP_TOKEN=your_meta_access_token
PHONE_NUMBER_ID=your_whatsapp_phone_number_id
VERIFY_TOKEN=your_secure_custom_verify_token

# Your GraphRAG Backend URL
GRAPH_RAG_API_URL=http://localhost:8000/chat


### Step 3: Run the Services
To test this locally, you will need to run your webhook server, expose it, and ensure your GraphRAG backend is running.

**Terminal 1: Start your GraphRAG API Backend**
*(This should be your main AI API repository)*

uvicorn api.server:app --host 0.0.0.0 --port 8000


**Terminal 2: Start the Webhook Server**

python webhook.py

*(The webhook server defaults to port 5001).*

**Terminal 3: Expose the Webhook with ngrok**

ngrok http 5001

*Copy the HTTPS URL provided by ngrok (e.g., `https://your-domain.ngrok-free.app`).*

## 🔗 Connect to Meta WhatsApp API

1. Go to your app's dashboard on Meta for Developers (https://developers.facebook.com/).
2. Navigate to **WhatsApp -> Configuration**.
3. Under the Webhook section, click **Edit**.
4. **Callback URL:** Paste your ngrok URL and append `/webhook` (e.g., `https://your-domain.ngrok-free.app/webhook`).
5. **Verify Token:** Enter the exact same `VERIFY_TOKEN` you set in your `.env` file.
6. Click **Verify and save**.
7. Click **Manage** under Webhook fields and subscribe to the `messages` event.

## 🧪 Testing the Pipeline
Send a message to your configured WhatsApp test number. 
1. The webhook server (`webhook.py`) should log the incoming payload.
2. It will forward the text to your GraphRAG API (`localhost:8000`).
3. Your GraphRAG agent will generate a response and send it back to the user on WhatsApp.
