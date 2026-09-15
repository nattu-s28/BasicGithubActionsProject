"""
Simple Todo API built with FastAPI.

This is intentionally kept simple (in-memory storage, no database) so that
students can focus on learning how GitHub Actions builds, tests, scans,
containerizes, and deploys a Python project — not on database setup.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API used to demonstrate a full "
    "GitHub Actions CI/CD pipeline.",
    version="1.0.0",
)

# In-memory "database" — a plain Python list of dicts.
# Resets every time the app restarts. Good enough for a learning project.
todos: List[dict] = []
next_id = 1


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class Todo(TodoCreate):
    id: int


@app.get("/", tags=["health"])
def read_root():
    """Health check / welcome route."""
    return {"message": "Todo API is running", "status": "ok"}


@app.get("/todos", response_model=List[Todo], tags=["todos"])
def list_todos():
    """Return every todo item."""
    return todos


@app.post("/todos", response_model=Todo, status_code=201, tags=["todos"])
def create_todo(todo: TodoCreate):
    """Create a new todo item."""
    global next_id
    new_todo = {"id": next_id, "title": todo.title, "done": todo.done}
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def get_todo(todo_id: int):
    """Return a single todo item by id."""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def update_todo(todo_id: int, updated: TodoCreate):
    """Update an existing todo item."""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = updated.title
            todo["done"] = updated.done
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204, tags=["todos"])
def delete_todo(todo_id: int):
    """Delete a todo item."""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
