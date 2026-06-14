from datetime import datetime
from pathlib import Path

import streamlit as st
from orchestrator import run_pipeline
from usajobs_api import fetch_usajobs

DEFAULT_RESUME_PATH = "job_hunt_assistant/data/default_resume.txt"

def parse_resume_output(path):
    try:
        with open(path, "r") as file:
            content = file.read().strip()
    except OSError:
        return "", ""

    if "<<RESUME_SUMMARY>>" in content and "<<COVER_LETTER>>" in content:
        summary_part = content.split("<<RESUME_SUMMARY>>", 1)[1]
        summary, cover = summary_part.split("<<COVER_LETTER>>", 1)
        return summary.strip(), cover.strip()

    return content, ""


def build_resume_output_path(job_index):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"job_hunt_assistant/data/resume_agent_output_{job_index}_{timestamp}.txt"


def load_default_resume(path=DEFAULT_RESUME_PATH):
    try:
        with open(path, "r") as file:
            return file.read().strip()
    except OSError:
        return ""


def write_default_resume_output(output_path, default_resume_text):
    content = (
        "<<RESUME_SUMMARY>>\n"
        f"{default_resume_text}\n\n"
        "<<COVER_LETTER>>\n"
        "Default fallback applied because AI tokens were exhausted. "
        "Please review and customize this before submitting."
    )
    path_obj = Path(output_path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with open(path_obj, "w") as file:
        file.write(content)


st.set_page_config(page_title="AI Job Hunt Assistant", layout="centered")

st.title("AI Job Hunt Assistant")
st.markdown("Use AI agents to analyze jobs, tailor your resume, and write outreach messages — all from one interface.")

# Input fields
keyword = st.text_input("Job Keyword", "business analyst")
location = st.text_input("Location", "New York")
resume_text = st.text_area("Paste Your Resume", height=200)
user_bio = st.text_area("Short Bio (for outreach tone)", "I’m a data professional passionate about public service.")

if "generated_files" not in st.session_state:
    st.session_state["generated_files"] = []

if st.button("Search Jobs"):
    job_posts = fetch_usajobs(keyword, location, results_per_page=5)
    if not job_posts:
        st.error("No job postings found for this search.")
        st.session_state.pop("jobs", None)
    else:
        st.session_state["jobs"] = job_posts
        st.success("Jobs fetched! Select the ones you'd like to apply for.")

if "jobs" in st.session_state:
    selected_indexes = []
    st.markdown("### Select Jobs to Apply For:")
    for i, job in enumerate(st.session_state["jobs"]):
        job_data = job.get("MatchedObjectDescriptor", {})
        title = job_data.get("PositionTitle", "Unknown Title")
        org = job_data.get("OrganizationName", "Unknown Agency")
        if st.checkbox(f"{title} - {org}", key=f"job_{i}"):
            selected_indexes.append(i)

    if st.button("Apply to Selected Jobs"):
        if not selected_indexes:
            st.warning("Please select at least one job.")
        elif not resume_text.strip():
            st.warning("Please paste your resume before applying.")
        else:
            for i in selected_indexes:
                job_data = st.session_state["jobs"][i].get("MatchedObjectDescriptor", {})
                title = job_data.get("PositionTitle", "Unknown Position")
                output_path = build_resume_output_path(i)
                with st.status(f"Applying to: {title}") as status:
                    result = run_pipeline(
                        job_data,
                        resume_text,
                        user_bio,
                        status_handler=status,
                        resume_output_path=output_path,
                    )
                    if result == "Try again later as you have exhausted your tokens.":
                        default_resume_text = load_default_resume()
                        if default_resume_text:
                            write_default_resume_output(output_path, default_resume_text)
                            if Path(output_path).exists():
                                st.session_state["generated_files"].append(output_path)

                            status.update(
                                label=f"Token limit reached for {title} - default resume applied",
                                state="complete",
                                expanded=False,
                            )
                            st.warning(
                                f"Token limit reached for {title}. "
                                "Applied fallback using job_hunt_assistant/data/default_resume.txt."
                            )

                            summary, cover_letter = parse_resume_output(output_path)
                            if summary:
                                st.markdown("#### Fallback Resume (Default)")
                                st.text_area(
                                    f"Default Resume ({title})",
                                    value=summary,
                                    height=180,
                                    key=f"default_resume_{i}",
                                )
                            if cover_letter:
                                st.markdown("#### Fallback Note")
                                st.text_area(
                                    f"Fallback Note ({title})",
                                    value=cover_letter,
                                    height=100,
                                    key=f"default_note_{i}",
                                )
                        else:
                            status.update(label=f"Token limit reached for {title}", state="error", expanded=False)
                            st.error(
                                f"Token limit reached for {title}, and default resume was not found at "
                                "job_hunt_assistant/data/default_resume.txt."
                            )
                    else:
                        status.update(label=f"Completed: {title}", state="complete", expanded=False)
                        if Path(output_path).exists():
                            st.session_state["generated_files"].append(output_path)
                        st.markdown("---")
                        st.markdown(f"### Outreach and analysis for: {title}")
                        st.markdown(str(result))

                        summary, cover_letter = parse_resume_output(output_path)
                        if summary:
                            st.markdown("#### Generated Resume Summary")
                            st.text_area(
                                f"Resume Summary ({title})",
                                value=summary,
                                height=140,
                                key=f"resume_summary_{i}",
                            )
                        if cover_letter:
                            st.markdown("#### Generated Cover Letter")
                            st.text_area(
                                f"Cover Letter ({title})",
                                value=cover_letter,
                                height=220,
                                key=f"cover_letter_{i}",
                            )

if st.session_state["generated_files"]:
    st.markdown("### Generated Files")
    recent_files = list(reversed(st.session_state["generated_files"][-10:]))
    for path in recent_files:
        st.write(path)