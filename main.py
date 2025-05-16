import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Critico de curriculos em IA", page_icon="📃", layout="centered")

st.title("Critico de curriculos em IA")
st.markdown("Faça o upload de seu curriculo para ter feedback com base em suas necessidades")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload do curriculo (PDF ou TXT)", type= ["pdf","txt"])
job_role = st.text_input("Escreva o cargo que almeja (opcional)")

analyze = st.button("Analizar curriculo")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text    

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content=extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("O arquivo não tem nenhum conteudo")
            st.stop()

        prompt = f"""Please analyze this resume and provide contructive feedback in brazilian portuguese.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for{job_role if job_role else 'general job aplications'}
        Resume content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations."""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=[
                {"role":"system","content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role":"user", "content": prompt }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown (response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occured:{str(e)}")


