import typer
from dotenv import load_dotenv, find_dotenv
from typing import Optional
from nexio.helpers.jobs import StoreOptions, JobsManagerTodoist

load_dotenv(find_dotenv())
app = typer.Typer()


@app.command()
def pull_jobs(store: StoreOptions = StoreOptions.no_store, output: Optional[str] = None):
    manager = JobsManagerTodoist()
    jobs = manager.get_jobs()
    manager.store(store_options=store, items=jobs, output=output)


@app.command()
def close_jobs():
    manager = JobsManagerTodoist()
    jobs = manager.get_jobs()
    manager.close_jobs(jobs=jobs)


if __name__ == '__main__':
    app()
