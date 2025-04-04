import streamlit as st
import fitz  # for PDF parsing
from openai import OpenAI  # import the new client class

# Initialize the OpenAI client with your API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("🧠 Reverse AI Interviewer")
st.write("Generate smart questions to ask your interviewer — based on your resume and role.")

# --- Upload Resume ---
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()

# --- Input Fields ---
role = st.text_input("What is the job title?", placeholder="e.g., Data Analyst")
company = st.text_input("What is the company name?", placeholder="e.g., Perchwell")

# --- Generate Questions ---
if st.button("Generate Interviewer Questions"):
    if uploaded_file and role and company:
        prompt = f"""
        You are a career coach. A candidate is interviewing for the role of '{role}' at '{company}'.
        Based on the candidate's resume below, generate 5 insightful and strategic questions they can ask the interviewer.
        These should reflect domain knowledge, curiosity, and cultural fit.

        Resume:
        {resume_text}
        """

        with st.spinner("Crafting your custom questions..."):
            # Updated API call using the client instance
            response = client.chat.completions.create(
                model="gpt-3.5",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            # Access the response content from the pydantic model
            questions = response.choices[0].message.content
            st.subheader("🎯 Questions to Ask the Interviewer:")
            st.markdown(questions)
    else:
        st.warning("Please upload your resume and enter both the job title and company name.")
