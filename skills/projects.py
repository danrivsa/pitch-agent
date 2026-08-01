from skills.skill_base import Skill
from utils.load_knowledge import load_knowledge


projects: Skill = {
    "name": "projects",
    "description": "Describes Daniel's notable projects in game development, robotics and AI, and home automation",
    "content": load_knowledge("projects.md")
}