from typing import TypedDict

class Skill(TypedDict):
    """
    Base class for skills.
    """
    name: str
    description: str
    content: str