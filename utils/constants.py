# utils/constants.py

info = {
    "name": "Keerthana ",

    # Title shown in the hero left column
    "title": "GenAI Engineer | LLMOps | Data Scientist",

    # Hero intro line (short, crisp, perfect for Split Gradient Hero)
    "Intro": (
        "I build reliable, user-friendly GenAI systems — RAG chatbots, "
        "LLMOps pipelines, and Streamlit demos that scale."
    ),
# About 
    "About": (
    "GenAI Engineer focused on building scalable, production-ready LLM applications. "
    "Specialize in RAG pipelines, LLMOps workflows, and interactive Streamlit demos that transform ideas into real-world AI solutions. "
    "Post-graduated in M.Sc Computer Science, completed a Data Science internship, and experienced in building AI/ML end-to-end applications. "
    "This AI portfolio is crafted in Streamlit to showcase my GenAI projects, RAG solutions, and LLMOps workflows in a simple, interactive way."
),


    "Email": "skeerthi.datascience@gmail.com",

    # profile image — will be auto-used if present in /images/
   
    "ProfileImage": "images/profile3.png",

    # badges for pill chips under hero intro
    "Badges": ["RAG", "LLMOps", "Streamlit", "Python", "SQL"],
}

# Social links (used in hero + contact section)
socials = {
    "GitHub": "https://github.com/Keerthana-DS-ghub",
    "LinkedIn": "https://www.linkedin.com/in/keerthana-datascience/",
}

embed_rss = {
    "enable": False,
    "rss": "",
}

# Optional placeholders for ML deployment preview
ML_BASE = ""
API_VERSION = ""
DEPLOYMENT_ID = ""

def get_iam_token_cached():
    """
    Preview stub: return None in preview mode.
    Replace with real implementation when deploying.
    """
    return None
