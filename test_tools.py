# In test_tools.py

from tools import parse_resumes, generate_embeddings, calculate_similarity, summarize_fit
import os
import numpy as np

# MockFile class stays the same
class MockFile:
    def __init__(self, path):
        self.name = path

# --- TEST SCRIPT ---
if __name__ == "__main__":
    print("--- Testing Full Chain + AI Summary Bonus ---")

    job_description = """
    Machine Learning Engineer
    
    We are seeking a hands-on Machine Learning Engineer with experience in Natural Language Processing (NLP).
    The ideal candidate will have strong Python skills and experience with robotics or automation projects.
    Experience with Gen AI and Large Language Models (LLMs) is a significant plus.
    """

    resume_folder = "sample_resumes"
    test_files = [MockFile(os.path.join(resume_folder, f)) for f in os.listdir(resume_folder)]
    
    if not test_files:
        print("No resumes found to test.")
    else:
        parsed_resumes = parse_resumes(test_files)
        
        # --- Steps 1, 2, 3: Rank Candidates (Same as before) ---
        resume_texts = [resume['text'] for resume in parsed_resumes]
        all_texts = [job_description] + resume_texts
        all_embeddings = generate_embeddings(all_texts)
        job_embedding = all_embeddings[0]
        candidate_embeddings = all_embeddings[1:]
        scores = calculate_similarity(job_embedding, candidate_embeddings)

        for i, resume in enumerate(parsed_resumes):
            resume['score'] = scores[i]

        ranked_results = sorted(parsed_resumes, key=lambda x: x['score'], reverse=True)

        print("\n--- Candidate Ranking ---")
        for i, result in enumerate(ranked_results):
            print(f"Rank {i+1}: {result['filename']} | Score: {result['score']:.2%}")

        # --- Step 4: Generate AI Summary for the Top Candidate ---
        print("\n--- AI Summary for Top Candidate ---")
        top_candidate = ranked_results[0]
        summary = summarize_fit(job_description, top_candidate['text'])
        
        print(f"Candidate: {top_candidate['filename']}")
        print("Summary:")
        print(summary)