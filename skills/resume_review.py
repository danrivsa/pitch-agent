from skills.skill_base import Skill
from utils.load_knowledge import load_knowledge


resume_review: Skill = {
    "name": "resume_review",
    "description": "Reviews Daniel's Resume (CV) to provide context for answering questions about his background, skills, and projects.",
    "content": load_knowledge("resume.md")
}