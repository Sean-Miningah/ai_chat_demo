
# 🧪 Crewmind.ai – Technical Challenge

Thank you for your interest in the **Lead Fullstack Developer** position at Nexa Consulting.

This short technical challenge is designed to reflect a simplified version of what we are building: an intelligent assistant that interacts via a frontend, stores memory, and returns contextual responses.

---

## 📌 Objective

Build a minimal fullstack assistant that allows a user to ask a question, stores it, and returns a (simulated) response.

---

## 🧱 Requirements

You are free to structure the code however you prefer, but the following features are expected:

### 1. Frontend – React
- A simple page with a **text input** and a **"Send" button**
- When clicked, the input should be sent to the backend via API
- Display the **response** from the backend on the screen

### 2. Backend – FastAPI
- Receive the question sent from the frontend
- Store the question in a **MongoDB** collection (local or cloud-based)
- Return a fixed simulated response:
  `"Thanks for your question, I’ll think about it."`

---

## ⚙️ Tech Stack Required

- Frontend: **React (JS or TS)**
- Backend: **FastAPI (Python)**
- Database: **MongoDB**

---

## 🧠 Bonus (optional but appreciated)
- Instead of a fixed response, dynamically generate it (e.g., via a public LLM API, dummy prompt logic, or local inference)
- Add a timestamp to each stored question
- Add a second endpoint `/history` to return the full conversation

---

## 📤 Submission Instructions

- Upload your code to **GitHub** and share the **repository link**
- Include a clear and concise **README** with:
  - How to run the frontend and backend
  - Which technologies/libraries you used
  - Anything you'd do differently with more time
- (Optional) Record a short **Loom video** (max 3 min) explaining your thought process

---

## 📅 Deadline

Please submit your GitHub link in maximum 3 days time period.
We’ll follow up shortly after reviewing your work.

---

## 🧭 Evaluation Criteria

We are not looking for perfection, but rather:
- Code clarity and structure
- Ability to use the right tools in the stack
- Autonomy and problem-solving approach
- Bonus: any sign of curiosity, creativity or care

Thank you again – we look forward to discovering your work!

## 🚀 How to Run the Solution

This project is containerized and can be run easily using Docker Compose.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Configuration

To enable dynamic AI responses, you need to configure the backend with your LLM provider credentials.

Open the `docker-compose.yml` file and locate the `environment` section for the `backend` service. Replace the placeholder values (`<API_URL_HERE>`, `<KEY_HERE>`, etc.) with your actual credentials.

**Example for OpenAI:**
```yaml
services:
  # ...
  backend:
    # ...
    environment:
      MONGODB_URL: mongodb://root:password@mongodb:27017/ai_chat?authSource=admin
      LLM_URL: https://api.openai.com/v1
      LLM_Model: gpt-3.5-turbo
      OPENAI_API_KEY: <YOUR_OPENAI_API_KEY>
      DATABASE_NAME: ai_chat
      COLLECTION_NAME: questions
```

- **`OPENAI_API_KEY`**: Your secret API key from OpenAI.
- **`LLM_URL`**: The base URL for the API. For OpenAI, this is `https://api.openai.com/v1`.
- **`LLM_Model`**: The model you wish to use, e.g., `gpt-3.5-turbo`.

> **Note**: If you do not provide an `OPENAI_API_KEY`, the application will fall back to providing predefined dummy responses.

### 2. Build and Run

From the root directory of the project, execute the following command to build and start all services:

```bash
docker-compose up --build
```

### 3. Access the Application

- **Frontend UI**: `http://localhost:3000`
- **Backend API Docs**: `http://localhost:8000/docs`

---

## 🛠️ Technologies & Libraries Used

This project is built with a modern, containerized stack:

-   **Backend**:
    -   **Framework**: FastAPI
    -   **Language**: Python
    -   **Database Driver**: PyMongo for MongoDB interaction.
    -   **LLM Integration**: OpenAI Python SDK for dynamic response generation.
    -   **Server**: Uvicorn ASGI server.

-   **Frontend**:
    -   **Framework**: React (with TypeScript) for a type-safe, component-based UI.
    -   **Styling**: Tailwind CSS for rapid, utility-first styling.
    -   **Build Tool**: Vite for a fast and modern development experience.

-   **Database**:
    -   MongoDB for flexible, document-based storage of conversation history.

-   **Infrastructure**:
    -   Docker & Docker Compose for consistent, isolated development and deployment environments.

---

## 🔮 What I'd Do With More Time

-   **Comprehensive AI Logging and Monitoring**: To better understand and manage the AI's performance and usage, I would implement a structured logging system. This would involve capturing key events for each AI interaction (question, response, latency, errors) on the backend. This data could then be fed into a monitoring tool like Datadog or Grafana to create dashboards for tracking usage patterns, API costs, and error rates, which is crucial for operational management.

---
