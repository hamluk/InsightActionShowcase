from pydantic import BaseModel

from src.app.prompts.prompt import create_insight_prompt, create_proposal_on_insight_prompt


class PromptLoader(BaseModel):
    _insight_prompt: str = create_insight_prompt
    _propose_action_prompt: str = create_proposal_on_insight_prompt

    @property
    def insight_prompt(self) -> str:
        return self._insight_prompt

    @insight_prompt.setter
    def insight_prompt(self, new_prompt: str):
        if all(word in new_prompt for word in ["{context}", "{format_instruction}"]):
            self._insight_prompt = new_prompt

    @property
    def propose_action_prompt(self) -> str:
        return self._propose_action_prompt

    @propose_action_prompt.setter
    def propose_action_prompt(self, new_prompt: str):
        if all(word in new_prompt for word in ["{format_instruction}", "{title}", "{summary}"]):
            self._propose_action_prompt = new_prompt