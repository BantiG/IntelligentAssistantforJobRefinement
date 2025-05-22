import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# prompt with LinkedIn-style format
def get_structured_job_ad_prompt(job_description):
    return f"""
You are a professional HR content writer.

Given the job description below, generate a polished and engaging job advertisement in the style of a LinkedIn job post with the following sections:

1. **About the job** – A brief summary of the position and company
2. **Responsibilities** – A bullet-point list of role responsibilities
3. **Qualifications** – Required education, experience, and skills
4. **Preferred Qualifications** – Nice-to-have experience/skills
5. **Benefits** – List of benefits/perks the candidate can expect (you may infer common ones if not provided)

Make it professional, inclusive, and engaging.

JOB DESCRIPTION:
{job_description}

Generate the output using Markdown formatting.
"""

# Prompt to generate screening questions
def get_screening_questions_prompt(job_description):
    return f"""
You are an expert technical recruiter.

Based on the job description below, generate 5 role-specific screening questions that can help assess candidates during the initial application phase.

Format them as a numbered list.

JOB DESCRIPTION:
{job_description}
"""

# Streamlit UI setup
st.set_page_config(page_title="AI - Job Role Optimizer", layout="centered")
st.title(" AI-Driven Job Role Optimizer")
st.write("Paste a job description to generate a LinkedIn-style job ad and role-specific screening questions.")

# Input text box
job_description = st.text_area(" Paste Job Description", height=300)

# Action button
if st.button(" Generate AI Content") and job_description:
    with st.spinner("Generating..."):

        # LinkedIn-style Job Ad
        job_ad_prompt = get_structured_job_ad_prompt(job_description)
        job_ad_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": job_ad_prompt}
            ]
        )
        job_ad = job_ad_response.choices[0].message.content

        # Screening Questions
        screening_prompt = get_screening_questions_prompt(job_description)
        screening_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": screening_prompt}
            ]
        )
        screening_questions = screening_response.choices[0].message.content

    # Output
    st.subheader(" AI Generated Job Advertisement")
    st.markdown(job_ad, unsafe_allow_html=True)

    st.subheader(" Screening Questions")
    st.text_area("Generated Questions", screening_questions, height=200)
