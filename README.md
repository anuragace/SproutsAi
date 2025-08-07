---
title: SproutsAI Candidate Recommender
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
license: apache-2.0
---

# SproutsAI - Candidate Recommendation Engine

**Developed by:** Anurag Kalapala  -  https://www.linkedin.com/in/anurag-kalapala-a03a28355/ 

**Live Demo:** [https://huggingface.co/spaces/Anuragleo67/SproutsAI](https://huggingface.co/spaces/Anuragleo67/SproutsAI)

---
## Project Overview

This project is a web application. The application serves as a tool for recruiters to efficiently find the best candidates for a job opening. It accepts a job description and a batch of candidate resumes, then intelligently ranks the candidates based on the semantic relevance of their resume to the job's requirements. To further assist recruiters, it also provides an AI-generated summary explaining why the top candidates are a strong match.

---
## Key Features

- **Multi-File Upload:** Accepts multiple resumes simultaneously in `.pdf`, `.docx`, and `.txt` formats.
- **Semantic Ranking:** Leverages a state-of-the-art sentence embedding model (`all-MiniLM-L6-v2`) to understand the contextual meaning of the text, going beyond simple keyword matching.
- **Relevance Scoring:** Computes the Cosine Similarity between the job description and each resume to provide a clear, quantitative relevance score.
- **AI-Powered Summaries:** Integrates with the Google Gemini API to provide concise, professional summaries for the top-ranked candidates, explaining their suitability for the role.
- **Interactive UI:** Built with Gradio for a clean, simple, and user-friendly web interface that requires no technical expertise to operate.

---
## My Approach & Design Choices

My core approach was to build a modular and robust application that was both effective and easy to maintain.

1.  **Modular, Tool-Based Architecture:** I designed the application using a modular architecture inspired by the Model Context Protocol (MCP). The core logic is separated into a `tools.py` file, containing four distinct, single-responsibility functions: a `Parser`, an `Embedder`, a `Similarity Calculator`, and an `AI Summarizer`. This separation of concerns makes the code clean, easy to test individually, and highly flexible. For example, this design allowed for a seamless switch from the OpenAI API to the Gemini API with zero changes to the application's main workflow.

2.  **Embedding Model:** I chose the `sentence-transformers/all-MiniLM-L6-v2` model for generating embeddings. It offers an excellent balance of high performance for semantic similarity tasks while remaining lightweight and fast, making it ideal for a real-time web application.

3.  **Generative AI for Summaries:** For the bonus task, I integrated the Gemini API (`gemini-1.5-flash-latest`). This powerful model is capable of understanding the nuanced relationship between a resume and a job description and generating human-like, insightful summaries that add significant value for a recruiter.

4.  **UI Framework:** I selected Gradio for the user interface. Its simplicity and focus on wrapping Python functions into web UIs allowed for rapid development and resulted in a clean, intuitive front-end for the demo.

---
## Assumptions

- **Text-Based Resumes:** The current implementation assumes that the uploaded resumes are text-based and parsable. It does not handle image-based or heavily formatted resumes.
- **Semantic Relevance as Primary Metric:** The ranking is based solely on the cosine similarity of text embeddings. It assumes this semantic relevance is the primary indicator of a good match for this initial screening phase.
- **Filename as ID:** For the purpose of this demo, the filename of the resume is used as the candidate's unique identifier.

---
## How to Run Locally

1.  **Clone the Repository**
    
    ```bash
    git clone <repository-url>
    cd <repository-directory-name>
    ```
    
2.  **Create and Activate a Virtual Environment**
    
    This keeps the project's dependencies isolated from other Python projects on your system.
    
    ```bash
    python -m venv venv
    ```
    
    Now, activate the environment.
    
    -   **On Windows:**
        
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        
    -   **On macOS/Linux:**
        
        ```bash
        source venv/bin/activate
        ```
        
3.  **Install Dependencies**
    
    This command reads the `requirements.txt` file and installs all the necessary libraries.
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Set the Environment Variable**
    
    The application requires a Google Gemini API key to generate summaries. You must set this as an environment variable.
    
    ```powershell
    $env:GOOGLE_API_KEY = "your-gemini-api-key"
    ```
    
5.  **Run the Application**
    
    ```bash
    python app.py
    ```
    
    After running the command, open your web browser and navigate to the local URL provided in the terminal, which is usually `http://127.0.0.1:7860`.
