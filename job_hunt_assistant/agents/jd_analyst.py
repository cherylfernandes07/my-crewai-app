# analyzing the job description
from crewai import Agent, Task, LLM
from job_hunt_assistant.utils.config import GEMINI_API_KEY


#Define a function named get_jd_analyst_agent() that returns a CrewAI Agent to summarize job descriptions.

def get_jd_analyst_agent(api_key=GEMINI_API_KEY, model_name="gemini/gemini-2.0-flash"):
    # Create an llm instance dynamically based on provided credentials
    llm = LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.2
    )

    return Agent(
        role="Job Description Analyst",
        goal="Understand and summarize government job postings",
        backstory="You're an expert in job market analysis with a focus on US federal job listings.",
        llm=llm,
        verbose=True
    )

# Define a function named create_jd_analysis_task() that:
# Accepts the agent and a job description as inputs.
def create_jd_analysis_task(agent, job_description):
    # Uses the Task class to construct a task that 
    # prompts the agent to extract key details from the job post.
    # Specifies a structured markdown output format.
    # Writes the final output to /data/report.md.    
    return Task(description=f"""
        Analyze the following USAJobs job posting and extract:
        - A summary of the role
        - Key skills required
        - Any specific qualifications or eligibility
        \n\nJob Description:\n{job_description}
        """,
        expected_output="A structured markdown summary containing sections for Qualifications, Required Skills, and Responsibilities.",
        agent=agent,
        output_file='data/report.md')
