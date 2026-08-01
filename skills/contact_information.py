from skills.skill_base import Skill
from utils.load_knowledge import load_knowledge


contact_information: Skill = {
    "name": "contact_information",
    "description": "Provides Daniel's contact details including LinkedIn, email, and Calendly scheduling link",
    "content": load_knowledge("contact_information.md")
}