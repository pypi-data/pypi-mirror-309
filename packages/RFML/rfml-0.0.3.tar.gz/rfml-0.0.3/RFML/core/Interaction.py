from enum import Enum


class TaskType(Enum):
    Train = 1
    Generate = 2
    Predict = 3
    Reload = 4


class Interaction:
    session_id: str
    model: str  # for API model train
    task: TaskType
    input: str

    def __init__(self, session_id: str, model: str, task: TaskType, user_input: str):
        self.session_id = session_id
        self.model = model
        self.task = task
        self.input = user_input
