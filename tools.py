# In tools.py

import os
import PyPDF2
import docx
from typing import List, Dict

# NOTE: For now, we are just defining the function.
# We will import and use Gradio later in the main app.py file.
# The type hint 'List[any]' is a placeholder for Gradio's file objects.

# --- Tool 1: Resume Parser ---
def parse_resumes(file_objects: List[any]) -> List[Dict[str, str]]:
    """
    Parses uploaded resume files (PDF, DOCX, TXT) and extracts text.
    
    Args:
        file_objects: A list of file objects, as provided by Gradio.
                      Each object has a .name attribute holding the temp file path.

    Returns:
        A list of dictionaries, where each dictionary contains the filename
        and the extracted text of a resume.
    """
    parsed_resumes = []
    if not file_objects:
        return []

    print(f"Starting to parse {len(file_objects)} files...")
    for file_obj in file_objects:
        file_path = file_obj.name
        filename = os.path.basename(file_path)
        text = ""
        
        # This block checks the file extension and uses the correct library to read it.
        try:
            if filename.endswith('.pdf'):
                # Open the PDF in binary read mode ('rb')
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or "" # Add 'or ""' to handle None
            
            elif filename.endswith('.docx'):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            
            elif filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

            # We only add the resume if we successfully extracted some text.
            if text.strip():
                parsed_resumes.append({'filename': filename, 'text': text})
                print(f"  Successfully parsed: {filename}")
            else:
                print(f"  Warning: No text extracted from {filename}")

        # This makes our tool robust. If one file is corrupted, the app won't crash.
        except Exception as e:
            print(f"  ERROR parsing {filename}: {e}")

    return parsed_resumes

# In tools.py (add this below the previous tool)

from sentence_transformers import SentenceTransformer
import numpy as np

# --- Tool 2: Embedding Generator ---
# We initialize the model outside the function. This is a crucial optimization.
# The model will be downloaded (first time only) and loaded into memory just once
# when the app starts, making every call to generate_embeddings very fast.
print("Loading SentenceTransformer model... (This may take a moment on first run)")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully.")

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generates sentence embeddings for a list of texts.

    Args:
        texts: A list of strings to be embedded.

    Returns:
        A numpy array of embedding vectors.
    """
    if not texts:
        return np.array([])
        
    try:
        print(f"Generating embeddings for {len(texts)} text(s)...")
        # The .encode() method does all the heavy lifting for us.
        embeddings = embedding_model.encode(texts, show_progress_bar=False)
        print("Embeddings generated successfully.")
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return np.array([])
    
    # In tools.py (add this below the previous tools)

from sklearn.metrics.pairwise import cosine_similarity

# --- Tool 3: Similarity Calculator ---
def calculate_similarity(target_embedding: np.ndarray, candidate_embeddings: np.ndarray) -> List[float]:
    """
    Calculates the cosine similarity between a target embedding and a list of candidate embeddings.

    Args:
        target_embedding: The embedding vector of the job description.
        candidate_embeddings: A numpy array of embedding vectors for the resumes.

    Returns:
        A list of cosine similarity scores.
    """
    if target_embedding is None or candidate_embeddings.size == 0:
        return []
    
    # scikit-learn's cosine_similarity expects 2D arrays for both arguments.
    # The target_embedding is currently a 1D array, so we reshape it to (1, 384)
    # to compare it against all candidate embeddings (which is already (n, 384)).
    target_embedding_2d = target_embedding.reshape(1, -1)
    
    scores = cosine_similarity(target_embedding_2d, candidate_embeddings)
    
    # The result is a 2D array [[score1, score2, ...]], so we extract the first row [0] to get a simple list.
    return scores[0].tolist()


import google.generativeai as genai

# --- Tool 4: AI Summarizer (Bonus) - NEW Gemini Version ---
def summarize_fit(job_description: str, resume_text: str) -> str:
    """
    Uses the Gemini LLM to generate a summary of why a candidate is a good fit.

    Args:
        job_description: The text of the job description.
        resume_text: The text of a single candidate's resume.

    Returns:
        A 2-3 sentence summary explaining the candidate's fit.
    """
    # Get the API key from your system's environment variables.
    # Note we are now looking for GOOGLE_API_KEY
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "ERROR: Google API key not found. Please set the GOOGLE_API_KEY environment variable."
    
    try:
        # Configure the library with your key
        genai.configure(api_key=api_key)

        # The prompt is the same as before!
        prompt = f"""
        You are an expert HR Talent Acquisition professional reviewing a resume for a job.
        Based on the following **Job Description** and **Candidate Resume** provided below, write a concise, 2-sentence summary explaining why this candidate is a strong fit for the role.
        Focus specifically on the alignment of their skills and experience with the key requirements mentioned in the job description.

        ---
        **Job Description:**
        {job_description}
        ---
        **Candidate Resume:**
        {resume_text}
        ---
        **Summary of Fit:**
        """
        
        # Initialize the model. We'll use 'gemini-1.5-flash' as it's fast and capable.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Generate the content
        response = model.generate_content(prompt)
        
        # Return the generated text
        return response.text.strip()
        
    except Exception as e:
        return f"Error generating summary with Gemini: {e}"