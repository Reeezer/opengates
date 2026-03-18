from logging import getLogger

from pydantic import BaseModel, ConfigDict

from opengates.ai_gateway.context import RequestContext
from opengates.ai_gateway.policy.resolver import BasePolicyResolver
from opengates.ai_gateway.registry import BaseModelRegistry
from opengates.messages import BaseMessage, TextMessageContent, UserMessage

__all__ = [
    "AIGateway",
]

logger = getLogger(__name__)


class AIGateway(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    model_registry: BaseModelRegistry
    policy_resolver: BasePolicyResolver

    def generate(
        self,
        context: RequestContext,
        model_name: str,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> str:
        # Get policy for request
        policy = self.policy_resolver.resolve(context)

        # Validate model access
        if not policy.validate_model_access(model_name):
            raise ValueError(f"Access to model {model_name} is not allowed")

        # Apply input guardrails
        history_list = self._format_history(history)
        for msg in history_list:
            for content in msg.content:
                if isinstance(content, TextMessageContent):
                    policy.apply_input_guardrails(content.text)

        # Generate response
        completion = self.model_registry.get(model_name=model_name)
        response = completion.generate(history_list)

        # Apply output guardrails
        policy.apply_output_guardrails(response)

        return response

    def _format_history(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> list[BaseMessage]:
        if isinstance(history, str):
            return [UserMessage(content=history)]
        elif isinstance(history, BaseMessage):
            return [history]
        elif isinstance(history, list):
            return history
        else:
            raise ValueError("Invalid history format")
