import re
import pandas as pd
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from nexio.helpers.todoist import TodoistHelper
from nexio.utils.postgres import Postgres


class StoreOptions(str, Enum):
    no_store = "no_store"
    csv = "csv"
    postgres = "postgres"


class TodoistProject(BaseModel):
    name: str = Field(description="Project Name", default="")
    id: str = Field(description="Project ID", default="")


class TodoistJob(BaseModel):
    name: str = Field(description="Job name", default="")
    saved_at: str = Field(description="Job saved date/time", default="")
    content: str = Field(description="Job content", default="")
    description: str = Field(description="Job description", default="")
    due_at: Optional[str] = Field(description="Job due date/time", default="")
    id: int = Field(description="Job ID", default="")
    label: List[str] = Field(description="Job labels", default="")
    order: int = Field(description="Job order", default=0)
    priority: int = Field(description="Job priority", default=0)
    project_id: str = Field(description="Job's project ID", default="")
    project_name: str = Field(description="Job's project name", default="")
    section_id: Optional[int] = Field(description="Job's section ID", default="")
    url: str = Field(description="Job's URL", default="")


class JobsManagerTodoist:
    def __init__(self):
        self._todoist_helper = TodoistHelper()
        self._project_parent = dict(name="214_job_search", id="2342935426")
        self._project_children = self._get_project_children()

    def _get_project_children(self):
        try:
            project_children = {}
            projects = self._todoist_helper.get_projects()
            for project in projects:
                if project.parent_id == self._project_parent['id']:
                    project_children[project.id] = project.name
            return project_children

        except Exception as e:
            raise f"Error fetching projects from Todoist: {e}"

    def get_jobs(self):
        project_ids = [project_id for project_id in self._project_children.keys()]
        tasks = self._todoist_helper.get_tasks(project_ids=project_ids)
        jobs = []
        for task in tasks:
            name, url = self._parse_content(content=task.content)
            jobs.append(TodoistJob(
                id=task.id,
                name=name,
                saved_at=task.created_at,
                content=task.content,
                description=task.description,
                due_at=str(task.due),
                label=task.labels,
                order=task.order,
                priority=task.priority,
                project_id=task.project_id,
                project_name=self._project_children.get(task.project_id),
                section_id=task.section_id,
                url=url,
            ))

        return jobs

    def close_jobs(self, jobs: List[TodoistJob]):
        task_ids = [str(job.id) for job in jobs]
        self._todoist_helper.close_tasks(task_ids=task_ids)

    @staticmethod
    def _parse_content(content):
        # Regular expression to extract the job_name and url
        pattern = r'\[(.*?)\]\((.*?)\)'

        # Use re.search to extract the groups
        match = re.search(pattern, content)

        if match:
            job_name = match.group(1)
            url = match.group(2)
            return job_name, url

        return "", ""

    @staticmethod
    def store(store_options: StoreOptions, items: List[TodoistJob], output: str):
        if store_options == StoreOptions.csv:
            JobsManagerTodoist._store_to_csv(items, output)

        if store_options == StoreOptions.postgres:
            JobsManagerTodoist._store_to_postgres(jobs=items)

    @staticmethod
    def _store_to_csv(items, output):
        if output is None:
            raise ValueError("Output cannot be None")

        items = [item.model_dump() for item in items]
        df = pd.DataFrame(items)
        # cols = ['name', 'saved_at', 'content', 'description', 'due_at', 'id', 'label',
        #         'order', 'priority', 'project_id', 'project_name', 'section_id', 'url'],
        new_order = ['id', 'name', 'order', 'project_name', 'url', 'saved_at', 'content', 'description', 'due_at',
                     'label', 'priority', 'project_id', 'section_id']
        df = df[new_order]
        df.to_csv(output, index=False)
        print(df.head(5))

    @staticmethod
    def _store_to_postgres(jobs: List[TodoistJob]):
        postgres = Postgres()
        postgres.connect()
        cursor = postgres.conn.cursor()

        insert_query = """
           INSERT INTO jobs (
               id, "order", name, url, label, saved_at, project_id, due_at, description, section_id, priority, content, project_name 
           ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (id) DO NOTHING;  -- Prevents duplicates based on 'id'
           """

        # Iterate over DataFrame rows and insert them
        for job in jobs:
            try:
                cursor.execute(insert_query, (
                    job.id,
                    job.order,
                    job.name,
                    job.url,
                    job.label,
                    job.saved_at,
                    job.project_id,
                    job.due_at,
                    job.description,
                    job.section_id,
                    job.priority,
                    job.content,
                    job.project_name,
                ))

            except Exception as e:
                raise Exception("Error on row {job.content}: {e}")

        postgres.conn.commit()
        cursor.close()
        postgres.conn.close()
