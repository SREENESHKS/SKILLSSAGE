%%writefile app.py
import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import re

GOOGLE_API_KEY = "ENTER API PLEASEEE"  # Replace if needed
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def extract_career_details(response_text):
    skill_match = re.search(r'\d+\.\s*(.+?)\s*–', response_text)
    job_match = re.search(r'Career:\s*(.+?)\s*\(', response_text)
    income_match = re.search(r'\((₹.+?/month.*?)\)', response_text)

    skill = skill_match.group(1).strip() if skill_match else "Skill"
    job = job_match.group(1).strip() if job_match else "Job"
    income = income_match.group(1).strip() if income_match else "₹20,000/month"

    return skill, job, income

def plot_career_path(skill="Digital Marketing", income="₹25,000/month", job="Entry-level Job"):
    steps = [
        "Identify Interest",
        f"Learn {skill}",
        "Do Freelance / Internship",
        f"Get {job}",
        f"Earn {income}"
    ]
    y = list(range(len(steps), 0, -1))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([1]*len(steps), y, marker='o', linewidth=2)
    for step, ypos in zip(steps, y):
        ax.text(1.01, ypos, step, fontsize=10, va='center')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("📈 Career Path")
    ax.axis('off')
    st.pyplot(fig)

def recommend_skills(user_input, language='english'):
    prompt = f"""
    You are SkillSage, an AI mentor for dropout students and underprivileged youth.

    Based on this input: "{user_input}", do the following:
    1. Suggest 3–5 practical skills or online courses they can learn.
    2. Give a short reason why each skill fits them.
    3. Mention a free/affordable learning platform (like Skill India, YouTube, Coursera, etc.).
    4. Suggest a career or job after learning each skill, with estimated salary/income in India.
    5. Draw a simple career path like:
        "Learn Skill → Do internship → Get job → Earn ₹X/month"
    6. Translate the full response to '{language}' if it's not English.
    Keep the tone friendly, motivational, and easy to understand.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_resume(name, education, skills, interests, courses, career_goal, language='english'):
    user_input = f"""
    Name: {name}
    Education: {education}
    Skills: {skills}
    Interests: {interests}
    Courses: {courses}
    Career Goal: {career_goal}
    """

    prompt = f"""
    You are SkillSage, an AI resume writer for underprivileged youth and school dropouts.
    Based on the following details, create a short, clear, friendly resume:
    --------------------
    {user_input}
    --------------------
    Use simple language. Translate to '{language}' if not English.

    Resume Format:
    --------------------
    Name:
    Objective:
    Education:
    Skills:
    Courses to Learn:
    Career Goal:
    --------------------
    """

    response = model.generate_content(prompt)
    return response.text

st.title("💡 SkillSage – AI Career Mentor")

with st.form("input_form"):
    user_input = st.text_input("Tell me your interest, past education or skill:")
    language = st.selectbox("Preferred language:", ["english", "hindi", "tamil", "malayalam"])
    submitted = st.form_submit_button("Get Career Guidance")

if submitted and user_input:
    st.subheader("🤖 Skill Suggestions")
    suggestions = recommend_skills(user_input, language)
    st.text(suggestions)

    skill, job, income = extract_career_details(suggestions)
    plot_career_path(skill, income, job)

with st.expander("📄 Generate Resume"):
    # Initialize session state variables if they don't exist
    if 'generate_resume_clicked' not in st.session_state:
        st.session_state.generate_resume_clicked = False
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""

    name = st.text_input("Your Name", key='name')
    education = st.text_input("Education", key='education')
    skills = st.text_input("Skills (comma separated)", key='skills')
    interests = st.text_input("Interests or dream career", key='interests')
    courses = st.text_input("Courses you want to learn", key='courses')
    goal = st.text_input("Career Goal", key='goal')

    if st.button("Generate Resume"):
        st.session_state.generate_resume_clicked = True
        # Call your generate_resume function here
        resume = generate_resume(
            name,
            education,
            skills,
            interests,
            courses,
            goal,
            language
        )
        st.session_state.resume_text = resume

    # Show resume only if button clicked
    if st.session_state.generate_resume_clicked:
        st.subheader("📝 Your Generated Resume")
        st.text(st.session_state.resume_text)
