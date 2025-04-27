import os
from groq import Groq
from dotenv import load_dotenv

from tools.job_tool import search_jobs
from tools.event_tool import get_events
from tools.mentor_tool import get_mentors
from pinecone_utils import semantic_search

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama3-70b-8192"  # Updated to a supported production model

# Prompt template
def build_prompt(user_query, rag_context):
    return f"""
You are Asha, an inclusive and helpful assistant for the JobsForHer Foundation platform.

Use the information below to answer the user's query as accurately and supportively as possible.

---
User Question:
{user_query}

---
Contextual Data from RAG:
{rag_context}

---
Your Answer (keep it clear, inclusive, and helpful):
"""

# Core function
def ask_asha(user_query: str) -> str:
    try:
        # Step 1: Semantic Search (temporarily disabled)
        rag_context = "No relevant context found from documents."
        
        # Step 2: Collect Tool Responses
        try:
            jobs = search_jobs(user_query) or []
        except Exception as e:
            print(f"[Job Tool Error] {e}")
            jobs = []

        try:
            events = get_events() or []
        except Exception as e:
            print(f"[Event Tool Error] {e}")
            events = []

        try:
            mentors = get_mentors() or []
        except Exception as e:
            print(f"[Mentor Tool Error] {e}")
            mentors = []

        # Step 3: Add Tool Data to Context
        rag_context += "\n\nRecent Job Listings:\n" + "\n".join(
            [f"- {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}" for job in jobs]
        )
        rag_context += "\n\nUpcoming Events:\n" + "\n".join(
            [f"- {event.get('title', 'Unknown')} on {event.get('date', 'Unknown')}" for event in events]
        )
        rag_context += "\n\nMentors:\n" + "\n".join(
            [f"- {mentor.get('name', 'Unknown')} ({mentor.get('expertise', 'Unknown')})" for mentor in mentors]
        )

        # Step 4: Prompt Construction
        prompt = build_prompt(user_query, rag_context)

        # Step 5: Groq LLM Call
        try:
            chat_completion = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"[Groq API Error] {e}")
            return "I couldn't connect to the language model. Please try again later."

    except Exception as e:
        print(f"[ask_asha Critical Error] {e}")
        return "Something went wrong processing your request."
