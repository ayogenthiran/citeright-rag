import streamlit as st

class CiteRightUI:
    def __init__(self):
        self.title = ""
        self.problem = ""
        self.seed_papers = []

    def render(self):
        st.title("📚 CiteRight – Literature Review Assistant")
        self.title = st.text_input("Title of your paper")
        self.problem = st.text_area("Short Problem Statement")
        seeds = st.text_area("Seed Papers (comma-separated arXiv IDs)", "")
        self.seed_papers = [s.strip() for s in seeds.split(",") if s]

        if st.button("Generate Literature Review"):
            return {
                "title": self.title,
                "problem": self.problem,
                "seed_papers": self.seed_papers
            }
        return None
