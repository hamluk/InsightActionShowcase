from src.app.config import Settings

def edit_prompt(
        insight_prompt: str,
        propose_action_prompt: str,
        settings: Settings
):
    settings.llm_model.prompts.insight_prompt = insight_prompt
    settings.llm_model.prompts.propose_action_prompt = propose_action_prompt

    return {
        "insight_prompt": settings.llm_model.prompts.insight_prompt,
        "propose_action_prompt": settings.llm_model.prompts.propose_action_prompt,
    }


def get_prompts(
    settings: Settings
):
    return {
        "insight_prompt": settings.llm_model.prompts.insight_prompt,
        "propose_action_prompt": settings.llm_model.prompts.propose_action_prompt,
    }