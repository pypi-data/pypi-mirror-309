import typer
import nexio.jobs
import nexio.todoist

app = typer.Typer()
app.add_typer(nexio.jobs.app, name="jobs")
app.add_typer(nexio.todoist.app, name="todoist")
