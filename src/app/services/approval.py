from src.app.config import Settings
from src.app.schemas.action import ActionProposal
from src.app.services.action import send_mail


def accept_approval(
        action_proposal: ActionProposal,
        settings: Settings,
):
    response = send_mail(action=action_proposal, email_settings=settings.mail)
    return response


def decline_approval(
        action_proposal: ActionProposal,
):
    return {
        "action": action_proposal.title,
        "status": "declined_by_human"
    }