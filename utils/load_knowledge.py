from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_knowledge(file_name: str) -> str:
	"""Return the contents of a markdown file from the knowledge directory."""
	knowledge_file = KNOWLEDGE_DIR / file_name

	if knowledge_file.suffix != ".md":
		knowledge_file = knowledge_file.with_suffix(".md")

	resolved_knowledge_dir = KNOWLEDGE_DIR.resolve()
	resolved_knowledge_file = knowledge_file.resolve()

	if resolved_knowledge_dir not in resolved_knowledge_file.parents:
		raise ValueError("Knowledge files must be loaded from the knowledge directory")

	if not resolved_knowledge_file.is_file():
		raise FileNotFoundError(f"Knowledge file not found: {knowledge_file.name}")

	return resolved_knowledge_file.read_text(encoding="utf-8")
