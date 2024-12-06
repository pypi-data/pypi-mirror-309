import typer
import os
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv, find_dotenv
from typing import Optional, List

from nexio.helpers.todoist import TodoistHelper, StoreOptions

load_dotenv(find_dotenv())
api = TodoistAPI(os.getenv('TODOIST_API_TOKEN'))

app = typer.Typer()


@app.command()
def get_projects(store: StoreOptions = StoreOptions.no_store):
    todoist_helper = TodoistHelper()
    projects = todoist_helper.get_projects()
    todoist_helper.store(store_options=store, items=projects, output="projects.csv")


@app.command()
def get_tasks(
        project_ids: Optional[List[str]] = None,
        store: StoreOptions = StoreOptions.no_store,
        output: str = None
   ):
    todoist_helper = TodoistHelper()
    if project_ids is not None:
        tasks = todoist_helper.get_tasks(project_ids=project_ids)
    else:
        tasks = todoist_helper.get_tasks()
    todoist_helper.store(store_options=store, items=tasks, output=output)

