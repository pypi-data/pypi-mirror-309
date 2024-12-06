""" Defines Task data model """

from datetime import datetime
from checks.utils import DATE_FORMAT, get_current_datetime


class Task:
    last_id = 0

    def __init__(self, description: str,
                 task_id: int = None,
                 completed: bool = False,
                 created_at=None,
                 completed_at=None) -> None:
        self.id = task_id or Task.get_next_id()
        self.description = description
        self.completed = completed
        self.created_at = created_at or get_current_datetime()
        self.completed_at = completed_at

        # Automatically add completed date if completed
        if completed and not completed_at:
            self.completed_at = get_current_datetime()

    @classmethod
    def from_dict(cls, data: dict):
        """ Convert `data` dictionary to Task object. """
        cls.update_last_id(data["id"])
        return cls(
            task_id=data['id'],
            description=data['description'],
            completed=data['completed'],
            created_at=data['created_at'],
            completed_at=data.get('completed_at')
        )

    def to_dict(self) -> dict:
        """ Convert Task object to a dictionary """
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def get_next_id(cls):
        cls.last_id += 1
        return cls.last_id

    @classmethod
    def update_last_id(cls, task_id):
        cls.last_id = max(cls.last_id, int(task_id))

    def __str__(self) -> str:
        return "%d: %s" % (self.id, self.description)
