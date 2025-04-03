import asyncio
import os
from pathlib import Path

from fastapi import BackgroundTasks

from aiconsole.core.project.project import choose_project


async def main():
    # Create project structure
    project_path = Path(os.getcwd())

    # Create necessary directories
    for dir_name in ["agents", "materials", "chats", ".aic"]:
        (project_path / dir_name).mkdir(exist_ok=True)

    # Initialize the project
    background_tasks = BackgroundTasks()
    await choose_project(project_path, background_tasks)

    print("Project initialized successfully!")


if __name__ == "__main__":
    asyncio.run(main())
