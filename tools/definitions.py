"""
tools/definitions.py
OpenAI-style function-calling tool schemas (JSON schema format).
Kept in sync with tools/langchain_tools.py.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_tushar_info",
            "description": (
                "Retrieve relevant information about Tushar Bansal from the portfolio "
                "knowledge base using semantic search (RAG). "
                "Use this tool for ANY question about Tushar's skills, projects, "
                "education, experience, certifications, or background."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Natural-language question or topic about Tushar "
                            "(e.g. 'What projects has Tushar built?')"
                        ),
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": (
                "Send a contact email to Tushar (the portfolio owner) on behalf of a visitor. "
                "Use this ONLY when the visitor explicitly wants to get in touch or send a message. "
                "The email is ALWAYS delivered to the owner — the recipient cannot be changed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full name of the visitor sending the message",
                    },
                    "email": {
                        "type": "string",
                        "description": "Visitor's email address (used as Reply-To only)",
                    },
                    "message": {
                        "type": "string",
                        "description": "The message content to send to the owner",
                    },
                },
                "required": ["name", "email", "message"],
            },
        },
    },
]
