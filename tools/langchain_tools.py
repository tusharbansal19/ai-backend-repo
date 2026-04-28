import os
from dotenv import load_dotenv
load_dotenv()
"""
tools/langchain_tools.py
LangChain @tool functions available to the portfolio agent.

Tools:
    1. send_email                 — contact Tushar on behalf of a visitor.
    2. get_tushar_academic_info   — academic background.
    3. get_tushar_profile         — general narrative.
    4. get_tushar_skills          — technical stack.
    5. get_tushar_projects        — project details.
    6. get_tushar_experience      — professional background.
    7. get_tushar_mentorship      — DSA mentorship info.
    8. get_tushar_certifications  — certifications and streaks.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.tools import tool


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
# Portfolio Information Tools (Pre-made messages)
# ──────────────────────────────────────────────────────────────────────────────

@tool
def get_tushar_academic_info() -> str:
    """
    Get information about Tushar Bansal's academic background, including his 
    degree, university (AKTU), CGPA (8.5), and school scores (Class 10/12).
    """
    return (
        "Tushar Bansal is currently pursuing a Bachelor of Technology in Computer Science "
        "from Dr. A.P.J. Abdul Kalam Technical University (2022–2026), maintaining an "
        "impressive CGPA of 8.5. He secured 90% in Class 12 (CBSE, Science) and 82.8% in Class 10. "
        "His academic foundation is built on a deep understanding of core CS subjects like DSA, "
        "Operating Systems, DBMS, and Software Engineering."
    )

@tool
def get_tushar_profile() -> str:
    """
    Get a general professional profile/narrative of Tushar Bansal.
    """
    return (
        "Tushar Bansal is a technically versatile Full Stack Developer specializing in "
        "scalable, production-grade applications using the MERN stack and Next.js. "
        "His development philosophy centers around performance, clean architecture, "
        "and user-centric design. He has a strong foundation in system design and "
        "real-time communication frameworks like Socket.IO."
    )

@tool
def get_tushar_skills() -> str:
    """
    Get a list of Tushar Bansal's technical skills, including programming languages, 
    frameworks, databases, and tools.
    """
    return (
        "Tushar's technical skill set includes:\n"
        "- Languages: Python, Java, JavaScript, C/C++\n"
        "- Frontend: React.js, Next.js, Tailwind CSS\n"
        "- Backend: Node.js, Express.js, NestJS\n"
        "- Databases: MongoDB, MySQL, PostgreSQL, Prisma ORM\n"
        "- Tools: Git, GitHub, Postman, Swagger, AWS (EC2, S3), CI/CD pipelines"
    )

@tool
def get_tushar_projects() -> str:
    """
    Get details about Tushar Bansal's key projects like SaatPherasWorldwide, 
    FastFinger, and Tushar Automobiles.
    """
    return (
        "Tushar has built several high-impact projects:\n"
        "1. SaatPherasWorldwide: A large-scale NRI-focused matrimonial platform with real-time chat (Socket.IO), JWT auth, and RBAC.\n"
        "2. FastFinger: A collaborative multiplayer typing application showcasing high-concurrency architecture and WebSockets.\n"
        "3. Tushar Automobiles: An SEO-driven e-commerce system built with Next.js, Prisma, and Redux, featuring SSR/SSG for max performance."
    )

@tool
def get_tushar_experience() -> str:
    """
    Get information about Tushar Bansal's professional experience and internships.
    """
    return (
        "Tushar worked as a Full Stack Developer intern at a Canada-based organization, "
        "where he built production-grade APIs, implemented JWT-based security guards, "
        "and optimized system reliability. He also served as a Team Lead for an academic "
        "internship project, guiding his team to build high-performance applications."
    )

@tool
def get_tushar_mentorship() -> str:
    """
    Get information about Tushar Bansal's experience as a DSA mentor.
    """
    return (
        "Tushar has successfully mentored over 70+ junior students in Data Structures "
        "and Algorithms (DSA). He designed structured learning sessions and emphasized "
        "pattern-based problem-solving. He was awarded an official mentorship certificate "
        "for his dedication and impact in fostering a strong learning culture."
    )

@tool
def get_tushar_certifications() -> str:
    """
    Get details about Tushar Bansal's certifications.
    """
    return (
        "Tushar holds certifications in:\n"
        "- Deep Learning from NVIDIA\n"
        "- Machine Learning from Infosys Springboard\n"
        "He is also a consistent coder on LeetCode with 50, 100, and 365-day streak badges."
    )


# ──────────────────────────────────────────────────────────────────────────────
# Exported tool list passed to the agent
# ──────────────────────────────────────────────────────────────────────────────
TOOLS = [
    send_email,
    get_tushar_academic_info,
    get_tushar_profile,
    get_tushar_skills,
    get_tushar_projects,
    get_tushar_experience,
    get_tushar_mentorship,
    get_tushar_certifications
]

