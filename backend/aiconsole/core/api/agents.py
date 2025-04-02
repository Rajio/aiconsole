from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from aiconsole.core.database.connection import get_db
from aiconsole.core.database.models import Agent
from aiconsole.core.database.services import AgentService

router = APIRouter()


@router.get("/agents", response_model=List[Agent])
async def get_agents(project_id: Optional[str] = None, owner_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Get list of agents with optional filtering by project or owner"""
    agent_service = AgentService(db)
    if project_id:
        return agent_service.get_project_agents(project_id)
    if owner_id:
        return agent_service.get_user_agents(owner_id)
    return []


@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get agent by ID"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/agents", response_model=Agent)
async def create_agent(
    name: str,
    system_prompt: str,
    project_id: str,
    owner_id: str,
    description: Optional[str] = None,
    temperature: str = "0.7",
    max_tokens: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    is_active: bool = True,
    db: Session = Depends(get_db),
):
    """Create a new agent"""
    agent_service = AgentService(db)
    return agent_service.create_agent(
        name=name,
        system_prompt=system_prompt,
        project_id=project_id,
        owner_id=owner_id,
        description=description,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        is_active=is_active,
    )


@router.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: str,
    name: Optional[str] = None,
    system_prompt: Optional[str] = None,
    description: Optional[str] = None,
    temperature: Optional[str] = None,
    max_tokens: Optional[str] = None,
    model: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """Update agent information"""
    agent_service = AgentService(db)
    update_data = {
        k: v
        for k, v in {
            "name": name,
            "system_prompt": system_prompt,
            "description": description,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "model": model,
            "is_active": is_active,
        }.items()
        if v is not None
    }
    agent = agent_service.update_agent(agent_id, **update_data)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """Delete agent"""
    agent_service = AgentService(db)
    if not agent_service.delete_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}
