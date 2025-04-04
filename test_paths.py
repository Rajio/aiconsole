from aiconsole.core.project.paths import get_project_directory
from aiconsole.core.project.project import is_project_initialized


def main():
    print("Is project initialized:", is_project_initialized())
    try:
        print("Project directory:", get_project_directory())
    except ValueError as e:
        print("Expected error:", e)


if __name__ == "__main__":
    main()
