import streamlit as st
from Models import get_embeddings, cosine

def compare(resume_texts, JD_text):
    JD_embeddings = None
    resume_embeddings = []

    if JD_text is not None:
        JD_embeddings = get_embeddings(JD_text)
    for resume_text in resume_texts:
        resume_embeddings.append(get_embeddings(resume_text))

    if JD_embeddings is not None and resume_embeddings is not None:
        cos_scores = cosine(resume_embeddings, JD_embeddings)
        return cos_scores
