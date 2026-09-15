"""
Test suite for the Todo API.

Run locally with:  pytest -v
These same tests run automatically inside the GitHub Actions CI workflow
on every push and pull request.
"""

from fastapi.testclient import TestClient
from app.main import app, todos

client = TestClient(app)


def setup_function():
    """Reset in-memory storage before every test so tests don't leak state."""
    todos.clear()


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_todo():
    response = client.post("/todos", json={"title": "Learn GitHub Actions"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn GitHub Actions"
    assert data["done"] is False
    assert "id" in data


def test_list_todos():
    client.post("/todos", json={"title": "First task"})
    client.post("/todos", json={"title": "Second task"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_todo():
    created = client.post("/todos", json={"title": "Read a book"}).json()
    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_missing_todo_returns_404():
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_update_todo():
    created = client.post("/todos", json={"title": "Old title"}).json()
    response = client.put(
        f"/todos/{created['id']}", json={"title": "New title", "done": True}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["done"] is True


def test_delete_todo():
    created = client.post("/todos", json={"title": "Delete me"}).json()
    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/todos/{created['id']}").status_code == 404
