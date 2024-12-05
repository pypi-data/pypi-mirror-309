from typing import Any, Type, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from agentlens.model import ModelUsage
from agentlens.provider import InferenceCost, Message, Provider

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(Provider):
    # Cost per million tokens in USD
    MODEL_COSTS = {
        "gpt-4o-mini": (0.150, 0.600),
        "gpt-4o-mini-2024-07-18": (0.150, 0.600),
        "gpt-4o": (5.00, 15.00),
        "gpt-4o-2024-08-06": (2.50, 10.00),
        "gpt-4o-2024-05-13": (5.00, 15.00),
        "o1-mini": (3.00, 12.00),
        "o1-mini-2024-09-12": (3.00, 12.00),
        "o1-preview": (15.00, 60.00),
        "o1-preview-2024-09-12": (15.00, 60.00),
    }

    def get_token_costs(self, model: str) -> tuple[float, float]:
        """Returns (input_cost_per_million, output_cost_per_million)"""
        return self.MODEL_COSTS.get(model, (0.0, 0.0))

    def _extract_usage(self, response: Any) -> ModelUsage:
        """Extract token usage from OpenAI response"""
        usage = getattr(response, "usage", None)
        if usage:
            return ModelUsage(
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            )
        return ModelUsage()

    def __init__(
        self,
        api_key: str | None = None,
        max_connections: dict[str, int] = {"DEFAULT": 10},
    ):
        super().__init__(name="openai", max_connections=max_connections)
        self.client = AsyncOpenAI(api_key=api_key)

    def _update_cost(
        self,
        model: str,
        response: Any,
        inference_cost: InferenceCost | None,
    ) -> None:
        if inference_cost is None:
            return

        usage = getattr(response, "usage", None)
        print(usage)
        if usage:
            input_cost_per_token, output_cost_per_token = self.get_token_costs(model)
            inference_cost.input_cost += usage.prompt_tokens * input_cost_per_token / 1_000_000
            inference_cost.output_cost += (
                usage.completion_tokens * output_cost_per_token / 1_000_000
            )

    async def generate_text(
        self,
        *,
        model: str,
        messages: list[Message],
        inference_cost: InferenceCost | None = None,
        **kwargs,
    ) -> str:
        completion = await self.client.chat.completions.create(
            model=model,
            messages=[m.model_dump() for m in messages],
            **kwargs,
        )

        self._update_cost(model, completion, inference_cost)
        assert completion.choices[0].message.content is not None
        return completion.choices[0].message.content

    async def generate_object(
        self,
        *,
        model: str,
        messages: list[Message],
        schema: Type[T],
        inference_cost: InferenceCost | None = None,
        **kwargs,
    ) -> T:
        completion = await self.client.beta.chat.completions.parse(
            model=model,
            messages=[message.model_dump() for message in messages],
            response_format=schema,
            **kwargs,
        )

        self._update_cost(model, completion, inference_cost)
        assert completion.choices[0].message.parsed is not None
        return completion.choices[0].message.parsed
