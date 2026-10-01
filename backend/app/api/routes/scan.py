"""POST /scan — the firewall endpoint the frontend calls.

Thin route: validate (via the schema) -> hand off to the scan service.
"""

from fastapi import APIRouter, Depends

from app.schemas import ScanRequest, ScanResponse
from app.services.scan_service import ScanService, get_scan_service

router = APIRouter(tags=["scan"])


@router.post(
    "/scan",
    response_model=ScanResponse,
    summary="Scan content for prompt injection",
    response_description="The firewall verdict, attack type, reason and confidence.",
)
async def scan(
    request: ScanRequest,
    service: ScanService = Depends(get_scan_service),
) -> ScanResponse:
    """Run the full firewall pipeline on the given content."""
    return await service.scan(request)
