from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field

# TODO: The models from this file are generated from private protos
# Here we just duplicate the models, but we should migrate the private
# protos to this repository to make them public


class ApplyTo(IntEnum):
    TEXT_BLOCK = 0
    FIELD = 1


class Filter(BaseModel):
    contains: list[str] = Field(default_factory=list)
    resource_type: list[str] = Field(default_factory=list)
    field_types: list[str] = Field(default_factory=list)
    not_field_types: list[str] = Field(default_factory=list)
    rids: list[str] = Field(default_factory=list)
    fields: list[str] = Field(default_factory=list)
    splits: list[str] = Field(default_factory=list)


class KBConfiguration(BaseModel):
    account: str = Field(default="")
    kbid: str = Field(default="")
    onprem: bool = Field(default=False)


class EntityDefinition(BaseModel):
    label: str = Field(description="Entity type")
    description: Optional[str] = Field(default="", description="Description of the entity type")


class EntityExample(BaseModel):
    name: str = Field(description="Name associated with the entity")
    label: str = Field(description="Type of entity")
    example: str = Field(default="", description="Example text where the entity is present")


class RelationExample(BaseModel):
    source: str = Field(description="Entity name from which the relation starts")
    target: str = Field(description="Entity name to which the relation ends")
    label: str = Field(description="Type of relation")
    example: str = Field(default="", description="Example text where the relation is present")


class GraphOperation(BaseModel):
    entity_defs: list[EntityDefinition] = Field(
        default_factory=list, description="Types of entities that will be considered for extraction"
    )
    entity_examples: list[EntityExample] = Field(
        default_factory=list, description="Examples of entities to be sent to the model as few-shot learning"
    )
    relation_examples: list[RelationExample] = Field(
        default_factory=list, description="Examples of relations to be sent to the model as few-shot learning"
    )
    ident: str = Field(default="", title="ID of Operation")


class Label(BaseModel):
    label: str = Field(default="")
    description: str = Field(default="")
    examples: list[str] = Field(default_factory=list)


class LabelOperation(BaseModel):
    labels: list[Label] = Field(default_factory=list)
    ident: str = Field(default="", title="ID of Operation")
    description: str = Field(default="")
    multiple: bool = Field(default=False)


class AskOperation(BaseModel):
    question: str = Field(default="")
    destination: str = Field(default="")
    json: bool = Field(default=False)  # type: ignore


class QAOperation(BaseModel):
    question_generator_prompt: str = Field(default="")
    system_question_generator_prompt: str = Field(default="")
    summary_prompt: str = Field(default="")
    generate_answers_prompt: str = Field(default="")


class ExtractOperation(BaseModel):
    class Model(IntEnum):
        TABLES = 0

    model: "ExtractOperation.Model" = Field(default=0)


class Operation(BaseModel):
    graph: Optional[GraphOperation] = Field(default=None, title="Graph Config")
    label: Optional[LabelOperation] = Field(default=None, title="Label Config")
    ask: Optional[AskOperation] = Field(default=None, title="Ask Config")
    qa: Optional[QAOperation] = Field(default=None, title="QA Config")
    extract: Optional[ExtractOperation] = Field(default=None, title="Extract Config")
    prompt_guard: Optional[bool] = Field(default=False, title="Prompt Guard Config")
    llama_guard: Optional[bool] = Field(default=False, title="Llama Guard Config")


class OpenAIKey(BaseModel):
    key: str = Field(default="")
    org: str = Field(default="")


class AzureOpenAIKey(BaseModel):
    key: str = Field(default="")
    url: str = Field(default="")
    deployment: str = Field(default="")
    model: str = Field(default="")


class HFLLMKey(BaseModel):
    class ModelType(IntEnum):
        LLAMA31 = 0
        QWEN25 = 1

    key: str = Field(default="")
    url: str = Field(default="")
    model: "HFLLMKey.ModelType" = Field(default=0)


class AzureMistralKey(BaseModel):
    key: str = Field(default="")
    url: str = Field(default="")


class PalmKey(BaseModel):
    credentials: str = Field(default="")
    location: str = Field(default="")


class MistralKey(BaseModel):
    key: str = Field(default="")


class AnthropicKey(BaseModel):
    key: str = Field(default="")


class TextGenerationKey(BaseModel):
    model: str = Field(default="")


class HFEmbeddingKey(BaseModel):
    """
    Some models require a specific template (including prefix) to work correctly in each task
    For example Snowflake's Arctic-embed requires a specific prefix to work correctly.
    In that case, the query prompt will be
    ```
    passage_prompt: ""
    query_prompt: "Represent this sentence for searching relevant passages: {}"
    ````
    where {} will be replaced by the actual sentence.
    `passage_prompt` is empty because the model does not require alterations to the sentence to embed is as a passage.
    """

    url: str = Field(default="")
    key: str = Field(default="")
    matryoshka: list[int] = Field(default_factory=list)
    similarity: str = Field(default="")
    size: int = Field(default=0)
    threshold: float = Field(default=0.0)
    passage_prompt: str = Field(default="")
    query_prompt: str = Field(default="")


class UserLearningKeys(BaseModel):
    openai: Optional[OpenAIKey] = Field(default=None)
    azure_openai: Optional[AzureOpenAIKey] = Field(default=None)
    palm: Optional[PalmKey] = Field(default=None)
    anthropic: Optional[AnthropicKey] = Field(default=None)
    claude3: Optional[AnthropicKey] = Field(default=None)
    text_generation: Optional[TextGenerationKey] = Field(default=None)
    mistral: Optional[MistralKey] = Field(default=None)
    azure_mistral: Optional[AzureMistralKey] = Field(default=None)
    hf_llm: Optional[HFLLMKey] = Field(default=None)
    hf_embedding: Optional[HFEmbeddingKey] = Field(default=None)


class OpenAIUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class AzureUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class HFUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class PalmUserPrompt(BaseModel):
    prompt: str = Field(default="")


class AnthropicUserPrompt(BaseModel):
    prompt: str = Field(default="")


class Claude3UserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class TextGenerationUserPrompt(BaseModel):
    prompt: str = Field(default="")


class MistralUserPrompt(BaseModel):
    prompt: str = Field(default="")


class AzureMistralUserPrompt(BaseModel):
    prompt: str = Field(default="")


class SummaryPrompt(BaseModel):
    prompt: str = Field(default="")


class UserPrompts(BaseModel):
    openai: Optional[OpenAIUserPrompt] = Field(default=None)
    azure_openai: Optional[AzureUserPrompt] = Field(default=None)
    palm: Optional[PalmUserPrompt] = Field(default=None)
    anthropic: Optional[AnthropicUserPrompt] = Field(default=None)
    text_generation: Optional[TextGenerationUserPrompt] = Field(default=None)
    mistral: Optional[MistralUserPrompt] = Field(default=None)
    azure_mistral: Optional[AzureMistralUserPrompt] = Field(default=None)
    claude3: Optional[Claude3UserPrompt] = Field(default=None)


class LLMConfig(BaseModel):
    model: str = Field(default="")
    provider: str = Field(default="")
    keys: Optional[UserLearningKeys] = Field(default=None)
    prompts: Optional[UserPrompts] = Field(default=None)


class DataAugmentation(BaseModel):
    name: str = Field(default="")
    on: ApplyTo = Field(default=0)
    filter: Filter = Field()
    operations: list[Operation] = Field(default_factory=list)
    llm: LLMConfig = Field()
