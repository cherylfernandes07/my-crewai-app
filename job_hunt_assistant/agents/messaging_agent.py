# drafting an outreach message
from crewai import Agent, Task, LLM
from job_hunt_assistant.utils.config import GEMINI_API_KEY  

#Define a function named get_messaging_agent that returns a new agent specialized in writing outreach messages for job seekers.

def get_messaging_agent():
    #Create an llm instance 
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=GEMINI_API_KEY,
        temperature=0.5
    )

    return Agent(
        role="Outreach Message Writer",
        goal="Draft personalized messages for job outreach",
        backstory="You're a professional career coach skilled in writing effective cold emails and outreach messages for job seekers in tech and government.",
        llm=llm,
        verbose=True
    )

#Define another function named create_messaging_task that returns a Task:
# Accept the agent, job summary, agency name, and user bio as inputs.

# Prompt the agent to write a brief, professional message expressing interest in the job.

# Specify an expected_output that keeps the response under 150 words and tailored for LinkedIn or email.
def create_messaging_task(agent, job_summary, agency_name, user_bio):
    return Task(
    description=f"""
    Write a concise and compelling outreach message that the candidate could send to someone at {agency_name}, expressing interest in the job described below.

    --- Job Summary ---
    {job_summary}

    --- Candidate Bio ---
    {user_bio}

    The message should be friendly, professional, and under 150 words. Tailor it for a platform like LinkedIn or email.
    """,
    expected_output="A short outreach message under 150 words, tailored for LinkedIn or email, that is professional and expresses interest in the job at the given agency.",
    agent=agent)
