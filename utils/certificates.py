# utils/certificates.py

certificates = [
    {
        "title": "Introduction to Generative AI",
        "issuer": "Duke University (Coursera)",
        "date": "Jun 2025",
        "image": "images/GenAI.png",
        "category": "GENAI"
    },
    {
        "title": "Generative AI Applications with RAG and LangChain",
        "issuer": "IBM (Coursera)",
        "date": "Jun 2025",
        "image": "images/Rag.png",
        "category": "GENAI"
    },
    {
        "title": "Tableau Certified Data Analyst",
        "issuer": "Udemy",
        "date": "Mar 2025",
        "image": "images/Tableau.jpg",
        "category": "DATA ANALYTICS"
    },
    {
        "title": "Master Data Science & AI Certified",
        "issuer": "Besant Technologies, Chennai",
        "date": "Oct 2025",
        "image": "images/Besant.png",
        "category": "DATA SCIENCE"
    },
    {
        "title": "Certificate of Internship",
        "issuer": "Zidio Development, Bangalore",
        "date": "01-08-2025 to 01-10-2025",
        "image": "images/Zidio_Intern.png",
        "category": "INTERNSHIP"
    },
    {
        "title": "Certificate of Training",
        "issuer": "Zidio Development, Bangalore",
        "date": "01-08-2025 to 01-10-2025",
        "image": "images/Zidio_Training.png",
        "category": "INTERNSHIP"
    }
]

def get_certificates():
    return certificates


def get_certificate_display_data():
    """
    Prepare certificate data for UI rendering.
    Keeps landing.py simple and bug-free.
    """
    out = []
    for c in certificates:
        out.append({
            "title": c.get("title", ""),
            "issuer": c.get("issuer", ""),
            "date": c.get("date", ""),
            "image": c.get("image", ""),
            "category": (c.get("category") or "").upper(),
        })
    return out


def certificates_as_text():
    """
    Convert certificates into plain text for AI chat context.
    """
    lines = []
    for c in certificates:
        title = c.get("title", "")
        issuer = c.get("issuer", "")
        date = c.get("date", "")
        category = (c.get("category") or "").upper()

        if category:
            lines.append(f"- {title} ({category}) by {issuer} ({date})")
        else:
            lines.append(f"- {title} by {issuer} ({date})")

    return "\n".join(lines)

