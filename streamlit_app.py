# The streamlit_app.py file is where you will build the user interface using Streamlit. 
# Learners can eventually input a job search keyword, paste their resume and bio, 
# and select jobs from a list to apply to. This will all be within a simple web interface.
import streamlit as st
from crewai import Agent, LLM
from job_hunt_assistant.utils.config import GEMINI_API_KEY
from usajobs_api import fetch_usajobs


llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=GEMINI_API_KEY
)

agent = Agent(
    role="Your role here",
    goal="Your goal here",
    backstory="Your backstory here",
    llm=llm
)

jobs = fetch_usajobs("business analyst", "New York", 10)

st.set_page_config(page_title="CrewAI App", page_icon="🤖")

st.title("🤖 CrewAI App")
st.write("Hello world! Your CrewAI agents will run here 123. ")

if jobs:
    st.success(f"{len(jobs)} jobs returned")
else:
    st.warning("No jobs returned")

if st.button("Run Agent ↗"):
    with st.spinner("Agent thinking..."):
        st.success("Agent complete! (replace this with your crew logic)")