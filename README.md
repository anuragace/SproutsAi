<<<<<<< HEAD
# SproutsAi
Candidate Recommendation Engine
=======
---
title: SproutsAi
emoji: 🦀
colorFrom: gray
colorTo: green
sdk: gradio
sdk_version: 5.41.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Candidate Recommendation Engine
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> 20659b7e722204bf396d8615c6247d166ebb3c3a

SproutsAI - Candidate Recommendation Engine
Submitted by: Anurag Kalapala

Live Demo: https://huggingface.co/spaces/Anuragleo67/SproutsAI

Project Overview
This project is a web application built to fulfill the take-home assignment for the Machine Learning Engineer Internship at SproutsAI. The application serves as a tool for recruiters to efficiently find the best candidates for a job opening. It accepts a job description and a batch of candidate resumes, then intelligently ranks the candidates based on the semantic relevance of their resume to the job's requirements. To further assist recruiters, it also provides an AI-generated summary explaining why the top candidates are a strong match.

Key Features
Multi-File Upload: Accepts multiple resumes simultaneously in .pdf, .docx, and .txt formats.

Semantic Ranking: Leverages a state-of-the-art sentence embedding model (all-MiniLM-L6-v2) to understand the contextual meaning of the text, going beyond simple keyword matching.

Relevance Scoring: Computes the Cosine Similarity between the job description and each resume to provide a clear, quantitative relevance score.

AI-Powered Summaries: Integrates with the Google Gemini API to provide concise, professional summaries for the top-ranked candidates, explaining their suitability for the role.

Interactive UI: Built with Gradio for a clean, simple, and user-friendly web interface that requires no technical expertise to operate.

My Approach & Design Choices
My core approach was to build a modular and robust application that was both effective and easy to maintain.

Modular, Tool-Based Architecture: I designed the application using a modular architecture inspired by the Model Context Protocol (MCP). The core logic is separated into a tools.py file, containing four distinct, single-responsibility functions: a Parser, an Embedder, a Similarity Calculator, and an AI Summarizer. This separation of concerns makes the code clean, easy to test individually, and highly flexible. For example, this design allowed for a seamless switch from the OpenAI API to the Gemini API with zero changes to the application's main workflow.

Embedding Model: I chose the sentence-transformers/all-MiniLM-L6-v2 model for generating embeddings. It offers an excellent balance of high performance for semantic similarity tasks while remaining lightweight and fast, making it ideal for a real-time web application.

Generative AI for Summaries: For the bonus task, I integrated the Gemini API (gemini-1.5-flash-latest). This powerful model is capable of understanding the nuanced relationship between a resume and a job description and generating human-like, insightful summaries that add significant value for a recruiter.

UI Framework: I selected Gradio for the user interface. Its simplicity and focus on wrapping Python functions into web UIs allowed for rapid development and resulted in a clean, intuitive front-end for the demo.

Assumptions
Text-Based Resumes: The current implementation assumes that the uploaded resumes are text-based and parsable. It does not handle image-based or heavily formatted resumes.

Semantic Relevance as Primary Metric: The ranking is based solely on the cosine similarity of text embeddings. It assumes this semantic relevance is the primary indicator of a good match for this initial screening phase.

Filename as ID: For the purpose of this demo, the filename of the resume is used as the candidate's unique identifier.

1. How to Run Locally
Clone the Repository:

git clone https://github.com/anuragace/SproutsAi.git
cd SproutsAi

2. Create and Activate a Virtual Environment:

python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

3. Install Dependencies:

pip install -r requirements.txt

4. Set Environment Variable: You must set your Google Gemini API key.

# In PowerShell:
$env:GOOGLE_API_KEY = "your-gemini-api-key"

5.Run the Application:

python app.py
Then open your browser to http://127.0.0.1:7860.