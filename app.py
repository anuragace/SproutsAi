# In app.py

import gradio as gr
import tools  # This imports all the functions from our tools.py file
import os

# --- 1. The Orchestrator Function ---
# This is the main function that Gradio will call. It orchestrates our tools.
def process_and_rank(job_description, resume_files):
    """
    Takes inputs from the Gradio UI, processes them using our tools,
    and returns a formatted string for display.
    """
    if not job_description or not resume_files:
        return "Please provide both a job description and at least one resume."

    # Use the tools
    parsed_resumes = tools.parse_resumes(resume_files)
    
    if not parsed_resumes:
        return "Could not parse any of the uploaded resumes. Please check the file formats."

    resume_texts = [resume['text'] for resume in parsed_resumes]
    
    # Embed all texts at once for efficiency
    all_texts = [job_description] + resume_texts
    all_embeddings = tools.generate_embeddings(all_texts)
    
    job_embedding = all_embeddings[0]
    candidate_embeddings = all_embeddings[1:]
    
    # Calculate scores
    scores = tools.calculate_similarity(job_embedding, candidate_embeddings)
    
    # Combine results and sort
    for i, resume in enumerate(parsed_resumes):
        resume['score'] = scores[i]
    
    ranked_results = sorted(parsed_resumes, key=lambda x: x['score'], reverse=True)
    
    # --- Format the Output for Display ---
    # We will use Markdown for a nice, clean presentation.
    output_string = f"## Top {len(ranked_results)} Candidates\n\n"
    
    for i, result in enumerate(ranked_results):
        output_string += f"### Rank {i+1}: {os.path.basename(result['filename'])}\n"
        output_string += f"**Relevance Score:** {result['score']:.2%}\n\n"
        
        # For the top 3 candidates, generate an AI summary
        if i < 3:
            output_string += "**AI Summary:**\n"
            summary = tools.summarize_fit(job_description, result['text'])
            output_string += f"> {summary}\n\n" # Using Markdown blockquote for the summary
        
        output_string += "---\n" # Separator
        
    return output_string

# --- 2. The Gradio Interface Definition ---
# This is where we define the web page layout.
interface = gr.Interface(
    fn=process_and_rank,  # The orchestrator function to call
    inputs=[
        gr.Textbox(lines=15, label="Job Description", placeholder="Paste the job description text here..."),
        gr.File(
            label="Upload Resumes",
            file_count="multiple",
            file_types=['.pdf', '.docx', '.txt']
        )
    ],
    outputs=gr.Markdown(label="Results"), # We use Markdown to display the formatted output
    title="SproutsAI Candidate Recommendation Engine",
    description="""
    Welcome! This tool helps you find the best candidates for a job.
    1. Paste the job description.
    2. Upload one or more resumes (PDF, DOCX, or TXT).
    3. Click 'Submit' to see the ranked candidates and an AI-generated summary of their fit.
    """,
    allow_flagging="never" # Disables the "Flag" button for a cleaner interface
)

# --- Launch the App ---
if __name__ == "__main__":
    # Before launching, ensure your API key is set as an environment variable!
    # For PowerShell: $env:GOOGLE_API_KEY = "your-key"
    interface.launch()