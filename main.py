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

uploaded_file = st-input.file_uploader("Upload do curriculo (PDF ou TXT)", type= ["pdf","txt"])
job_role = st.text_input("Escreva o cargo que almeja (opcional)")

analyze = st.button("Analizar curriculo")

def extract_text_from_pdf(pdf_file):
    def_reader = PyPDF.PdfReader(pdf_file)
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
