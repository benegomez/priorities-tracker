from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.projects.api.schemas import (
    AvailablePhaseItem, MemberAdd, MemberResponse, OwnerInfo,
    PhaseCreate, PhaseResponse, PhaseUpdate,
    ProjectCreate, ProjectDetailResponse, ProjectListItem, ProjectListResponse, ProjectUpdate,
)
from src.modules.projects.domain.entities.project import VALID_PROJECT_TRANSITIONS, Project
from src.modules.projects.domain.entities.phase import VALID_PHASE_TRANSITIONS, ProjectPhase
from src.modules.projects.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import BusinessRuleViolation

router = APIRouter(prefix="/projects", tags=["projects"])


def _require_admin_or_manager(current_user: CurrentUser):
    if current_user.role not in ("administrator", "manager"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators and managers can manage projects")


@router.get("/phases/available", response_model=list[AvailablePhaseItem], summary="Get available phases for priority form")
async def get_available_phases(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[AvailablePhaseItem]:
    repo = ProjectRepositoryImpl(session)
    rows = await repo.get_available_phases(current_user.organization_id)
    return [AvailablePhaseItem(id=r.id, name=r.name, project_name=r.project_name) for r in rows]


@router.get("/org-members", response_model=list[dict], summary="List organization members for selects")
async def get_org_members(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    _require_admin_or_manager(current_user)
    from sqlalchemy import text as sql_text
    result = await session.execute(
        sql_text("""
            SELECT id, first_name || ' ' || last_name as full_name, role, email
            FROM users
            WHERE organization_id = :org_id AND status = 'active' AND deleted_at IS NULL
            ORDER BY first_name, last_name
        """),
        {"org_id": current_user.organization_id},
    )
    return [{"id": str(r.id), "full_name": r.full_name, "role": r.role, "email": r.email} for r in result.fetchall()]


@router.get("", response_model=ProjectListResponse, summary="List projects")
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> ProjectListResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)
    rows, total = await repo.list_by_org(current_user.organization_id, status_filter, page, page_size)
    items = [
        ProjectListItem(
            id=r.id, name=r.name, description=r.description, status=r.status,
            owner=OwnerInfo(id=r.owner_id, full_name=r.owner_name) if r.owner_id else None,
            phases_count=r.phases_count, members_count=r.members_count, created_at=r.created_at,
        )
        for r in rows
    ]
    return ProjectListResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=ProjectDetailResponse, status_code=status.HTTP_201_CREATED, summary="Create project")
async def create_project(
    body: ProjectCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> ProjectDetailResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    if not await repo.user_belongs_to_org(body.owner_id, current_user.organization_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner must belong to the same organization")

    project_id = uuid4()
    await repo.save_project(project_id, current_user.organization_id, body.owner_id, body.name, body.description)

    return ProjectDetailResponse(
        id=project_id, name=body.name, description=body.description, status="draft",
        owner=OwnerInfo(id=body.owner_id, full_name=""),
        phases=[], members=[],
    )


@router.get("/{project_id}", response_model=ProjectDetailResponse, summary="Get project detail")
async def get_project_detail(
    project_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> ProjectDetailResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    project = await repo.get_by_id(project_id, current_user.organization_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    phases = await repo.get_phases(project_id, current_user.organization_id)
    members = await repo.get_members(project_id, current_user.organization_id)

    return ProjectDetailResponse(
        id=project.id, name=project.name, description=project.description, status=project.status,
        owner=OwnerInfo(id=project.owner_id, full_name=project.owner_name) if project.owner_id else None,
        phases=[PhaseResponse(id=p.id, name=p.name, status=p.status) for p in phases],
        members=[MemberResponse(user_id=m.user_id, full_name=m.full_name, role=m.role) for m in members],
        created_at=project.created_at, updated_at=project.updated_at,
    )


@router.patch("/{project_id}", response_model=ProjectDetailResponse, summary="Update project")
async def update_project(
    project_id: UUID,
    body: ProjectUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> ProjectDetailResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    project = await repo.get_by_id(project_id, current_user.organization_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Validate state transition
    if body.status and body.status != project.status:
        p = Project(id=project.id, organization_id=current_user.organization_id, owner_id=project.owner_id, name=project.name, status=project.status)
        try:
            p.change_status(body.status)
        except BusinessRuleViolation as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    # Validate owner
    if body.owner_id and not await repo.user_belongs_to_org(body.owner_id, current_user.organization_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner must belong to the same organization")

    fields = {k: v for k, v in body.model_dump(exclude_none=True).items()}
    if fields:
        await repo.update_project(project_id, current_user.organization_id, **fields)

    return await get_project_detail(project_id, current_user, session)


@router.post("/{project_id}/phases", response_model=PhaseResponse, status_code=status.HTTP_201_CREATED, summary="Create phase")
async def create_phase(
    project_id: UUID,
    body: PhaseCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PhaseResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    project = await repo.get_by_id(project_id, current_user.organization_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    phase_id = uuid4()
    await repo.save_phase(phase_id, current_user.organization_id, project_id, body.name)
    return PhaseResponse(id=phase_id, name=body.name, status="planned")


@router.patch("/{project_id}/phases/{phase_id}", response_model=PhaseResponse, summary="Update phase")
async def update_phase(
    project_id: UUID,
    phase_id: UUID,
    body: PhaseUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PhaseResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    phase_row = await repo.get_phase(phase_id, current_user.organization_id)
    if phase_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phase not found")

    # Validate state transition
    if body.status and body.status != phase_row.status:
        phase = ProjectPhase(id=phase_row.id, organization_id=current_user.organization_id, project_id=project_id, name=phase_row.name, status=phase_row.status)
        try:
            phase.change_status(body.status)
        except BusinessRuleViolation as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    fields = {k: v for k, v in body.model_dump(exclude_none=True).items()}
    if fields:
        await repo.update_phase(phase_id, current_user.organization_id, **fields)

    updated = await repo.get_phase(phase_id, current_user.organization_id)
    return PhaseResponse(id=updated.id, name=updated.name, status=updated.status)


@router.post("/{project_id}/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED, summary="Add member")
async def add_member(
    project_id: UUID,
    body: MemberAdd,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> MemberResponse:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    project = await repo.get_by_id(project_id, current_user.organization_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not await repo.user_belongs_to_org(body.user_id, current_user.organization_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User must belong to the same organization")

    if await repo.member_exists(current_user.organization_id, project_id, body.user_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a member of this project")

    member_id = uuid4()
    await repo.add_member(member_id, current_user.organization_id, project_id, body.user_id)

    # Get user info for response
    result = await session.execute(
        __import__("sqlalchemy").text("SELECT first_name || ' ' || last_name as full_name, role FROM users WHERE id = :id"),
        {"id": body.user_id},
    )
    user = result.one()
    return MemberResponse(user_id=body.user_id, full_name=user.full_name, role=user.role)


@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove member")
async def remove_member(
    project_id: UUID,
    user_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    _require_admin_or_manager(current_user)
    repo = ProjectRepositoryImpl(session)

    if not await repo.member_exists(current_user.organization_id, project_id, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    await repo.remove_member(current_user.organization_id, project_id, user_id)
