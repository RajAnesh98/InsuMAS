# InsuMas: AI-Powered Insurance Assistant

InsuMas is an advanced, multi-agent AI system designed to provide comprehensive assistance for insurance-related queries. Built with Python, LangChain, and Gradio, this application leverages a sophisticated supervisor-agent architecture to intelligently route user requests to a team of specialized AI agents. Whether you need to understand complex insurance terms, find a suitable plan, calculate costs, or locate a doctor, InsuMas offers a seamless and interactive experience.

## ✨ Features

*   **Multi-Agent Architecture**: A central supervisor agent analyzes user queries and delegates them to the most appropriate specialist agent, ensuring efficient and accurate responses.
*   **Comprehensive Insurance Support**:
    *   **Insurance Info Agent**: Fetches specific details about insurance plans from a knowledge base.
    *   **Plan Recommendation Agent**: Provides personalized insurance plan recommendations based on user demographics and needs.
    *   **Cost Calculator Agent**: Estimates out-of-pocket expenses for medical procedures.
    *   **FAQ Agent**: Answers common questions and defines insurance terminology.
*   **Healthcare Provider Search**:
    *   **Doctor Recommender Agent**: Finds and suggests local doctors based on specialty and location.
*   **Empathetic Interaction**:
    *   **Optimism Agent**: Provides emotional support and encouragement when users express frustration or stress.
*   **Retrieval-Augmented Generation (RAG)**: Utilizes ChromaDB vector databases to provide agents with relevant, up-to-date information from external knowledge bases.
*   **Interactive Web UI**: A user-friendly interface built with Gradio that supports text input, image uploads, and audio recording.

## 🏛️ Architecture

The project is structured around a modular, agentic framework:

*   **Frontend**: The user interface is built with **Gradio**, providing an interactive chat experience.
*   **Backend Core**: **LangChain** and **LangGraph** provide the fundamental framework for creating and connecting the agents.
*   **Supervisor Agent**: The central router (`Supervisor_Agent.py`) that interprets the user's intent and directs the conversation to a sub-agent.
*   **Specialist Sub-Agents**: Each agent in the `Agents/` directory is a specialist with a distinct role and access to a specific set of tools.
*   **Language Model**: Powered by **Groq** for fast and efficient language processing (`Agents/LLM.py`).
*   **Knowledge Base**: **ChromaDB** is used for efficient vector storage and retrieval, enabling the RAG capabilities (`RAG/` directory).
*   **Tools**: A collection of Python functions (`tools.py`) that agents use to perform actions, such as querying databases or performing calculations.

## 📂 File Structure

```
InsuMas/
├── Agents/                  # Contains all agent logic and definitions
├── RAG/                     # RAG scripts and ChromaDB databases
├── .gitignore
├── main.py                  # Main application entrypoint with Gradio UI
├── prompts.py               # All prompts for the agents and supervisor
├── requirements.txt         # Project dependencies
├── Supervisor_Agent.py      # Logic for the main supervisor agent
└── tools.py                 # Tools available to the agents
```

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

*   Python 3.9 or higher
*   Git

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/InsuMas.git
    cd InsuMas
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

This project requires an API key from Groq to power the language model.

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Groq API key to the `.env` file as follows:

    ```
    GROQ_API_KEY="your_groq_api_key_here"
    ```

    *Note: The application is coded to automatically load this environment variable.*

### 4. Running the Application

Once the setup is complete, you can start the Gradio web server.

1.  Run the `main.py` script from your terminal:
    ```bash
    python main.py
    ```

2.  The terminal will display a local URL (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser to interact with the InsuMas assistant.

### 5. (Optional) Rebuilding the Databases

The repository includes pre-built ChromaDB vector databases. If you modify the source data or need to rebuild them, you can run the provided scripts.

```bash
# To rebuild the insurance knowledge base
python RAG/RAG_Insurance_Dataset.py

# To rebuild the doctor directory
python RAG/RAG_Doctor_Dataset.py
```
