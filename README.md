# 🏏 Chiku-AI: Agentic IPL War-Room
**Next-Gen Tactical Intelligence for Cricket Operations**

[![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-blue?style=for-the-badge&logo=googlegemini)](https://deepmind.google/technologies/gemini/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React.js-61DAFB?style=for-the-badge&logo=react)](https://reactjs.org/)

## 🛰️ Project Overview
Chiku-AI is an **Agentic Command Center** designed to bridge the gap between raw cricket telemetry and actionable tactical intelligence. Built for the Google Solution Challenge 2026, it leverages the **Gemini 1.5 Pro** engine to perform real-time reasoning over live match data and historical IPL datasets (278k+ deliveries).

---

## 🧠 Architectural Intelligence (How it Works)

The system operates on an **Agentic Loop** rather than a static pipeline:

1.  **Telemetry Ingestion:** Real-time extraction of match states via `pycricbuzz` and BigQuery.
2.  **Context Augmentation:** Live data is fused with historical player archetypes using the `Chiku-Brain` (CSV-based RAG Lite).
3.  **Reasoning Layer:** Gemini 1.5 Pro analyzes the current game state (Score, RR, Batsman Tendencies) to generate **Tactical Alerts**.
4.  **Sentiment Engine:** A dynamic feedback loop that calculates "Stadium Vibe" by analyzing real-time social sentiment.
5.  **Reactive UI:** An "Origami-style" high-fidelity dashboard that visualizes predictions through a WebSocket stream.

---

## 🛠️ Tech Stack

### **Backend (The Core Engine)**
* **FastAPI:** High-performance asynchronous framework for handling concurrent WebSocket connections.
* **Gemini-Google-AI:** Powering reasoning for tactical decision-making.
* **LangChain/Chiku-Engine:** Manages the state and flow of AI responses.
* **PyCricbuzz:** Wrapper for live match data acquisition.

### **Frontend (The Command Interface)**
* **React.js:** Component-driven architecture for a modular UI.
* **Framer Motion:** Powering physics-based animations (VibeMeter & Prediction Wheel).
* **WebSockets:** Ensuring sub-100ms latency for live updates.
* **Web Speech API:** Integrated Voice-AI for hands-free tactical updates.

---

## 📂 System Structure
```text
├── Backend/
│   ├── main.py          # WebSocket Orchestrator & API Routes
│   ├── agents.py        # Gemini Agent Logic & Prompt Engineering
│   ├── database.py      # Data Pre-processing & Historical Analysis
│   └── deliveries_updated_ipl_upto_2025.csv  # The "Knowledge Base"
├── Frontend/
│   ├── src/
│   │   ├── App.js       # Global State & Socket Management
│   │   └── components/  # Predictive Wheel & Sentiment Meter
