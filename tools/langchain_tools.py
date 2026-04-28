import os
from dotenv import load_dotenv
load_dotenv()
"""
tools/langchain_tools.py
LangChain @tool functions available to the portfolio agent.

Only the two requested tools are exported:
    1. send_email      — contact Tushar on behalf of a visitor.
    2. get_tushar_info — RAG retrieval over the portfolio knowledge base.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.tools import tool
from rag.retriever import format_context_for_prompt, retrieve_context


# ──────────────────────────────────────────────────────────────────────────────
# Tool 1 — Email (always to owner only, never to any other address)
# ──────────────────────────────────────────────────────────────────────────────
@tool
def send_email(name: str, email: str, message: str) -> str:
    """
    Send a contact email to Tushar (the portfolio owner) on behalf of a visitor.
    Use this ONLY when the visitor explicitly wants to reach out, get in touch,
    or send a message. The email is always delivered to the owner — no other
    recipient is ever used.

    Args:
        name    : Full name of the visitor sending the message.
        email   : Visitor's email address (used as Reply-To only).
        message : The message content the visitor wants to send.
    """
    sender_email    = os.getenv("SMTP_USER", "")
    sender_password = os.getenv("SMTP_PASSWORD", "")

    if not sender_email or not sender_password:
        return (
            "❌ Email service is not configured right now. "
            f"Please reach out to {os.getenv('OWNER_NAME', 'Tushar')} directly."
        )

    # Hard-coded recipient: always owner — never accept dynamic recipients
    recipient = os.getenv("OWNER_EMAIL", "")
    if not recipient:
        return "❌ Owner email not configured. Cannot send message."

    msg = MIMEMultipart("alternative")
    msg["Subject"]  = f"Portfolio Contact: Message from {name}"
    msg["From"]     = sender_email
    msg["To"]       = recipient          # always owner's email
    msg["Reply-To"] = email              # visitor's email just for reply-to

    body = (
        f"New contact request from portfolio AI:\n\n"
        f"Name:    {name}\n"
        f"Email:   {email}\n"
        f"Message:\n{message}\n"
        f"\n— Portfolio AI Agent"
    )
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", "587"))) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
        return (
            f"✅ Your message has been sent to {os.getenv('OWNER_NAME', 'Tushar')}! "
            f"They'll get back to you at {email} soon. 😊"
        )
    except Exception as exc:
        return f"❌ Failed to send email: {str(exc)}"


# ──────────────────────────────────────────────────────────────────────────────
# Tool 2 — RAG retrieval (portfolio knowledge base)
# ──────────────────────────────────────────────────────────────────────────────
@tool
def get_tushar_info(query: str) -> str:
    """
    Retrieve relevant information about Tushar Bansal from the portfolio
    knowledge base using semantic search (RAG).

    Use this tool whenever a visitor asks about:
      - Tushar's skills, technologies, or tech stack
      - His projects (SaatPherasWorldwide, FastFinger, Tushar Automobiles, etc.)
      - His education (AKTU, CGPA, Class 10/12 scores)
      - His professional experience (internship, team lead)
      - His DSA mentorship (70+ students)
      - His certifications (NVIDIA Deep Learning, Infosys ML)
      - His GitHub, LeetCode streaks, or any personal/professional background
      - General "who is Tushar?" or "tell me about Tushar" questions

    Args:
        query : A natural-language question or topic about Tushar.

    Returns:
        Formatted context string from the portfolio knowledge base,
        or a fallback message if no relevant information is found.
    """
    chunks = retrieve_context(query)
    print("TOOL CALLING HAPPEN >..................", chunks)
    if not chunks:
        return (
            f"I couldn't find specific information about that in my knowledge base. "
            f"Please ask a more specific question about {os.getenv('OWNER_NAME', 'Tushar')}'s skills, projects, education, or experience."
        )
    return format_context_for_prompt(chunks)


# ──────────────────────────────────────────────────────────────────────────────
# Exported tool list passed to the agent
# ──────────────────────────────────────────────────────────────────────────────
TOOLS = [send_email , get_tushar_info]
