from skills.resume_review import resume_review
from skills.skill_base import Skill
from skills.contact_information import contact_information
from skills.projects import projects

SKILLS: list[Skill] = [
    resume_review,
    contact_information,
    projects
]