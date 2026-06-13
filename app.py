import streamlit as st
from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

agent = Agent(
    role="Your role here",
    goal="Your goal here",
    backstory="Your backstory here",
    llm=llm
)

st.set_page_config(page_title="CrewAI App", page_icon="🤖")

st.title("🤖 CrewAI App")
st.write("Hello world! Your CrewAI agents will run here 123. ")

if st.button("Run Agent ↗"):
    with st.spinner("Agent thinking..."):
        st.success("Agent complete! (replace this with your crew logic)")