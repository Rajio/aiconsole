print("Testing imports...")

print("1. Importing from paths...")
from aiconsole.core.project.paths import get_project_directory

print("   OK")

print("2. Importing from project...")
from aiconsole.core.project.project import is_project_initialized

print("   OK")

print("All imports successful!")
