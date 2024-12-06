from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

from nuclia_models.common.utils import BaseConfigModel
from nuclia_models.worker.proto import ApplyTo, DataAugmentation


class ApplyOptions(str, Enum):
    """
    Defines how the tasks should be applied to the existing data.
    - EXSITING: Only apply to existing data (starts a worker that executes the task)
    - NEW: Only apply to new data (enables the task at processing time)
    - ALL: Apply to all data (both of the above)
    """

    EXISTING = "EXISTING"
    NEW = "NEW"
    ALL = "ALL"


class TaskName(str, Enum):
    DUMMY = "dummy"
    ENV = "env"
    DEMO_DATASET = "demo-dataset"
    LABELER = "labeler"
    LLM_GRAPH = "llm-graph"
    SYNTHETIC_QUESTIONS = "synthetic-questions"
    ASK = "ask"
    LLM_ALIGN = "llm-align"
    SEMANTIC_MODEL_MIGRATOR = "semantic-model-migrator"


class JobStatus(str, Enum):
    NOT_RUNNING = "not_running"
    FINISHED = "finished"
    RUNNING = "running"
    STARTED = "started"
    STOPPED = "stopped"
    FAILED = "failed"


class SemanticModelMigrationParams(BaseModel):
    semantic_model_id: str = Field(
        description="The id of the semantic model to migrate to. This must be a valid semantic model id available for the account"
    )


class TaskValidation(BaseModel):
    validation: Optional[type[BaseModel]] = None
    available_on: list[ApplyTo] = []

    def custom_validation(self, name: TaskName, parameters: Optional[BaseModel]) -> "TaskValidation":
        validation_class = self.validation if self.validation is not None else type(None)
        if not isinstance(parameters, validation_class):
            if self.validation is None:
                raise ValueError(f"Task {name.value} parameters must be null")
            else:
                raise ValueError(
                    f"Task {name.value} parameters must match the {self.validation.__name__} model."
                )
        if isinstance(parameters, DataAugmentation):
            if parameters.on not in self.available_on:
                raise ValueError(f"Can not run task on {parameters.on} can only run on {self.available_on}")
            if len(parameters.operations) == 0:
                raise ValueError("At least one operation must be defined")

        return self


TASKS: dict[TaskName, TaskValidation] = {
    TaskName.DUMMY: TaskValidation(),
    TaskName.ENV: TaskValidation(),
    TaskName.DEMO_DATASET: TaskValidation(),
    TaskName.LABELER: TaskValidation(
        validation=DataAugmentation,
        available_on=[ApplyTo.TEXT_BLOCK, ApplyTo.FIELD],
    ),
    TaskName.LLM_GRAPH: TaskValidation(
        validation=DataAugmentation,
        available_on=[ApplyTo.FIELD],
    ),
    TaskName.SYNTHETIC_QUESTIONS: TaskValidation(
        validation=DataAugmentation,
        available_on=[ApplyTo.FIELD],
    ),
    TaskName.ASK: TaskValidation(
        validation=DataAugmentation,
        available_on=[ApplyTo.FIELD],
    ),
    TaskName.LLM_ALIGN: TaskValidation(
        validation=DataAugmentation,
    ),
    TaskName.SEMANTIC_MODEL_MIGRATOR: TaskValidation(
        validation=SemanticModelMigrationParams,
        available_on=[ApplyTo.FIELD],
    ),
}


class TaskStart(BaseConfigModel):
    name: TaskName
    parameters: Optional[Union[DataAugmentation, SemanticModelMigrationParams]] = Field(
        description="Parameters to be passed to the task. These must match the `validation` field for the Task definition class",
    )

    @model_validator(mode="after")
    def validate_parameters(self) -> "TaskStart":
        task: Optional[TaskValidation] = TASKS.get(self.name)
        if task is None:
            raise ValueError(f"There is no task defined for {self.name.value}")

        task.custom_validation(name=self.name, parameters=self.parameters)
        return self


class TaskStartKB(TaskStart):
    apply: ApplyOptions = Field(
        default=ApplyOptions.ALL,
        description=ApplyOptions.__doc__,
    )


class TaskResponse(BaseModel):
    name: TaskName
    status: JobStatus
    id: str
