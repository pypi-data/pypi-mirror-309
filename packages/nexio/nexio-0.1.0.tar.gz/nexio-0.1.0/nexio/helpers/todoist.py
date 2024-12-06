import os
import pandas as pd
from typing import Optional, List
from enum import Enum

from todoist_api_python.models import Project, Task
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv, find_dotenv
from rich import print
from rich.progress import track

load_dotenv(find_dotenv())


class StoreOptions(str, Enum):
    no_store = "no_store"
    csv = "csv"
    postgres = "postgres"


class TodoistHelper:
    def __init__(self):
        self.api = TodoistAPI(os.getenv('TODOIST_API_TOKEN'))

    def get_projects(self):
        try:
            projects = self.api.get_projects()
            return projects

        except Exception as error:
            raise f"Error getting projects: {error}"

    def get_tasks(self, project_ids: Optional[List[str]] = None):
        try:
            tasks = []
            if project_ids is None:
                tasks.extend(self.api.get_tasks())

            # If project_ids provided, use them to filter tasks
            else:
                for project_id in project_ids:
                    tasks.extend(self.api.get_tasks(project_id=project_id))

            return tasks

        except Exception as error:
            raise f"Error getting tasks: {error}"

    def close_tasks(self, task_ids: Optional[List[str]] = None):
        try:
            if task_ids is None:
                raise Exception(f"task_ids not provided and the tasks cannot be closed")

            for task_id in track(task_ids):
                is_success = self.api.close_task(task_id)
                if is_success:
                    print(f"task_id {task_id} successfully closed")

        except Exception as error:
            raise error

    @staticmethod
    def store(store_options: StoreOptions, items: List[Project] | List[Task], output: str):
        if store_options == StoreOptions.csv:
            if output is None:
                raise ValueError("Output cannot be None")

            items = [item.__dict__ for item in items]
            df = pd.DataFrame(items)
            df.to_csv(output, index=False)
            print(df.head(5))

        if store_options == StoreOptions.postgres:
            raise NotImplementedError("Storing to postgres is not implemented yet")
