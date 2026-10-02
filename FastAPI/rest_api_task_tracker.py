"""
Objective: You're building a small REST API for a task tracker using Python (Flask or FastAPI, your choice). Implement the endpoints for a `tasks` resource:

- `GET /tasks` returns all tasks
- `GET /tasks/{id}` returns one task, or a 404 if it doesn't exist
- `POST /tasks` creates a task from a JSON body like `{"title": "Write tests"}` and returns the created task
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Data model for Tasks
class Task(BaseModel):
    title: str

# In memory dictionary storage for Tasks
tasks = []

@app.get("/tasks/", status_code=200)
def getTasks():
    return tasks

@app.get("/tasks/{id}/", status_code=200)
def getTask(id:int):
    if id < 0 or id > len(tasks):
        return JSONResponse(status_code=404, content=f"No Task For ID: {id}")
    return tasks[id]

@app.post("/tasks/", status_code=201)
def postTask(task: Task):
    tasks.append(task)
    return { "id": len(tasks), "task": task }