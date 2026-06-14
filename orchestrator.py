import time
from crewai import Crew, Process
import job_hunt_assistant.agents.jd_analyst as jd_analyst
import job_hunt_assistant.agents.resume_cl_agent as resume_cl_agent
import job_hunt_assistant.agents.messaging_agent as messaging_agent
from job_hunt_assistant.utils.tracking import log_application, save_cover_letter_file
import usajobs_api as usajobs_api
from job_hunt_assistant.utils.config import GEMINI_API_KEY, GEMINI_API_KEY_2


def extract_between_markers(text, start, end=None):
    try:
        start_idx = text.index(start) + len(start)
        end_idx = text.index(end, start_idx) if end else len(text)
        return text[start_idx:end_idx].strip()
    except ValueError:
        return "Not found"

def run_pipeline(
    job_data,
    resume_text,
    user_bio,
    status_handler=None,
    resume_output_path="job_hunt_assistant/data/resume_agent_output.txt",
):
    job_summary = job_data.get("UserArea", {}).get("Details", {}).get("JobSummary")
    agency_name = job_data.get("OrganizationName", "Unknown Agency")
    job_title = job_data.get("PositionTitle", "Unknown Position")

    if not job_summary:
        return "The selected job is missing a JobSummary."
    if not resume_text.strip():
        return "Please provide your resume text before applying."

    max_retries = 3
    retry_delay = 5  # Initial delay in seconds

    for attempt in range(max_retries):
        # Update UI message on retries
        if attempt > 0 and status_handler:
            status_handler.update(label=f"Retrying analysis for {job_title}...", state="running")

        # Determine which configuration to use
        active_key = GEMINI_API_KEY
        active_model = "gemini/gemini-2.0-flash"

        # Switch to the fallback key on retry, but keep using a supported model.
        if attempt > 0 and GEMINI_API_KEY_2:
            active_key = GEMINI_API_KEY_2
            active_model = "gemini/gemini-2.0-flash"

        # Step 3: Initialize agents
        # Step 4: Create tasks
        jd_analyst_agent = jd_analyst.get_jd_analyst_agent(api_key=active_key, model_name=active_model)
        jd_task = jd_analyst.create_jd_analysis_task(jd_analyst_agent, job_summary)

        resume_writer_agent = resume_cl_agent.get_resume_cl_agent()
        resume_task = resume_cl_agent.create_resume_cl_task(
            resume_writer_agent,
            job_summary,
            resume_text,
            output_file=resume_output_path,
        )

        message_agent = messaging_agent.get_messaging_agent()
        message_task = messaging_agent.create_messaging_task(message_agent, job_summary, agency_name, user_bio)

        # Step 5: Create and run the crew
        crew = Crew(
            agents=[jd_analyst_agent, resume_writer_agent, message_agent],
            tasks=[jd_task, resume_task, message_task],
            process=Process.sequential
        )

        try:
            result = crew.kickoff()

            # Extract key outputs from the resume task for tracking artifacts.
            resume_output = str(resume_task.output) if resume_task.output is not None else ""
            resume_summary = extract_between_markers(
                resume_output,
                "<<RESUME_SUMMARY>>",
                "<<COVER_LETTER>>",
            )
            cover_letter = extract_between_markers(resume_output, "<<COVER_LETTER>>")

            log_application(job_title, agency_name, resume_summary)
            save_cover_letter_file(job_title, cover_letter)

            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Double the wait time for the next attempt
                    continue
                return "Try again later as you have exhausted your tokens."
            return f"An unexpected error occurred: {e}"


def run_pipeline_from_search(keyword="business analyst", location="New York", results_per_page=1):
    jobs = usajobs_api.fetch_usajobs(keyword, location, results_per_page)
    if not jobs:
        return f"No jobs were returned for '{keyword}' in '{location}'."

    job = jobs[0]
    job_data = job.get("MatchedObjectDescriptor", {})
    return run_pipeline(job_data, resume_text="", user_bio="")


if __name__ == "__main__":
    result = run_pipeline_from_search()
    print("\n=== FINAL OUTPUT ===\n")
    print(result)