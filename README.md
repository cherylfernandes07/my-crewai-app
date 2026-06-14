# CrewAI Job Application Assistant

Build modular AI agents using CrewAI and LangChain.
Orchestrate collaborative, task-specific agent workflows with CrewAI.
Create a web-based interface for your agent workflow using Streamlit.
Use large language models to generate structured, customized content.

## Overview

The job market is competitive, and nearly every employer now expects AI skills. Instead of just talking about AI proficiency, why not demonstrate it by building an AI-powered job application assistant that automates your entire job search? In this project, we'll create a multi-agent system using CrewAI, Python, and Streamlit that handles everything from analyzing job descriptions to drafting personalized LinkedIn outreach messages, saving time while showcasing your AI workflow automation capabilities to potential employers.

## How it Works

We'll build specialized AI agents using the CrewAI framework: a job analyzer that extracts key requirements from listings, a resume customization agent that tailors application materials, and a messaging agent that drafts professional outreach. We'll orchestrate these autonomous agents into a collaborative crew where each agent's output feeds into the next, creating an intelligent automation pipeline powered by LangChain and Google Gemini for natural language processing. We'll integrate the USAJobs API to fetch real government job postings and provide live data for the agents to work with.

## Features
Finally, we'll develop a Streamlit web application where you can input job preferences, browse fetched listings, select target positions, and generate customized resumes, cover letters, and LinkedIn messages with one click. We'll implement persistent logging to track applications and save generated materials. By the end, you'll have a portfolio-ready agentic system demonstrating CrewAI multi-agent orchestration, API integration, LLM-powered automation, and practical AI agent collaboration that proves your AI skills to recruiters.

## Project Structure

- `streamlit_app.py`: The frontend UI built with Streamlit.
- `orchestrator.py`: The core logic that manages the CrewAI workflow and agent handoffs.
- `usajobs_api.py`: Handles interaction with the USAJobs Search API.
- `job_hunt_assistant/agents/`: Definitions for the JD Analyst, Resume Writer, and Messaging agents.
- `job_hunt_assistant/utils/`: Utility functions for tracking, logging, and configuration.
- `job_hunt_assistant/data/`: Storage for generated cover letters, application logs, and default templates.

## Getting Started

Follow these steps to set up and run the application locally:

1. **Configuration:**
   Create a configuration file or environment variables for the following keys:
   - `GEMINI_API_KEY`: Primary key for Google Gemini 2.0 Flash.
   - `GEMINI_API_KEY_2`: Fallback key for rate limiting/retries.
   - `USAJOBS_API_KEY`: Required to fetch live job data from USAJobs.gov.

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Managing the environment:**
   When you're done working, deactivate with:
   ```bash
   deactivate
   ```
   And every time you come back to the project, just run `source venv/bin/activate` again before anything else.