# writing the resume and cover letter,
from crewai import Agent, Task, LLM
from job_hunt_assistant.utils.config import GEMINI_API_KEY


#Define a function get_resume_cl_agent() that returns a new agent, 
# configured for resume and cover letter writing.
def get_resume_cl_agent():
    #Create an llm instance using ChatGoogleGenerativeAI, configured to use the gemini-2.0-flash model and your Gemini API key with a slightly higher temperature than the JD agent for more creativity.
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=GEMINI_API_KEY,
        temperature=0.4
    )

    return Agent(
    role="Resume and Cover Letter Writer",
    goal="Customize application materials to match job descriptions",
    backstory="You're an expert in professional writing and tailoring resumes for job applications, especially in government and tech roles.",
    llm=llm,
    verbose=True
    )

# Define the create_resume_cl_task() function that constructs and returns a Task object with the following specifications:

# The function accepts agent, job_summary, and resume_text as input parameters.

# It builds a prompt that instructs the agent to:

# Tailor the candidate’s resume summary.

# Generate a personalized cover letter suitable for a government job.

# Includes distinct output markers (<<RESUME_SUMMARY>>, <<COVER_LETTER>>) to support downstream parsing.

# Writes the final output to job_hunt_assistant/data/resume_agent_output.txt.
def create_resume_cl_task(
    agent,
    job_summary,
    resume_text,
    output_file="job_hunt_assistant/data/resume_agent_output.txt",
):
    return Task(
        description=f"""
        Based on the job summary below, tailor the candidate's resume summary and generate a personalized cover letter.
        
        --- Job Summary ---
        {job_summary}
        
        --- Resume Text ---
        {resume_text}
        
        Your output should include:
        1. Updated professional summary for resume
        2. A personalized cover letter suitable for a government job
        """,
        agent=agent,
        expected_output="""
        <<RESUME_SUMMARY>>
        [Your tailored 3-5 sentence resume summary here]

        <<COVER_LETTER>>
        [Your personalized cover letter here]
        """,        
        output_file=output_file)

