from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.ai_insights.api.schemas import DataSnapshot, TeamSummaryRequest, TeamSummaryResponse
from src.modules.ai_insights.application.commands.generate_team_summary import GenerateTeamSummaryUseCase
from src.modules.ai_insights.infrastructure.openai_client import OpenAIClient
from src.modules.auth.api.dependencies import CurrentUser, get_current_user, require_roles
from src.shared.database.session import get_db_session

router = APIRouter(prefix="/ai", tags=["ai"])

_openai_client = OpenAIClient()


@router.post(
    "/team-summary",
    response_model=TeamSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate weekly team summary",
    description="Generates an AI-powered executive summary of the manager's team for the current week. Uses cache if available.",
    operation_id="generate_team_summary",
    responses={
        403: {"description": "Insufficient permissions"},
    },
)
async def generate_team_summary(
    body: TeamSummaryRequest = TeamSummaryRequest(),
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> TeamSummaryResponse:
    use_case = GenerateTeamSummaryUseCase(session=session, openai_client=_openai_client)
    result = await use_case.execute(
        manager_id=current_user.user_id,
        organization_id=current_user.organization_id,
        regenerate=body.regenerate,
    )
    return TeamSummaryResponse(
        summary=result.summary,
        generated_at=result.generated_at,
        model=result.model,
        data_snapshot=DataSnapshot(**result.data_snapshot),
        fallback=result.fallback,
        cached=result.cached,
    )
