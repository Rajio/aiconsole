from pathlib import Path

import tomli

AGENTS_DIR = Path(__file__).parent


def load_agent(agent_name: str) -> dict:
    """Load agent configuration from .toml file"""
    agent_path = AGENTS_DIR / f"{agent_name}.toml"
    if not agent_path.exists():
        raise FileNotFoundError(f"Agent {agent_name} not found")

    with open(agent_path, "rb") as f:
        return tomli.load(f)


def get_all_agents() -> list[str]:
    """Get list of all available agents"""
    return [f.stem for f in AGENTS_DIR.glob("*.toml")]
