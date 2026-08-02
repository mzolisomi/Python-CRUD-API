# Python CRUD API

This is a basic CRUD Python web API to comprehend the HTTP methods and explore how they work under the hood.

Command to install app:

```git
pip install fastapi uvicorn
```

To run the app:

```git
uv run fastapi dev
```

Table of endpoints:

| Method | Endpoint            | Description                                                                 | Success Response | Error Responses                          |
|--------|----------------------|-------------------------------------------------------------------------------|-------------------|-------------------------------------------|
| GET    | `/`                  | Returns a simple welcome message                                              | `200 OK`          | —                                         |
| GET    | `/health`            | Returns basic API metadata (name, version, available endpoints)              | `200 OK`          | —                                         |
| GET    | `/tasks`             | Returns the full list of tasks                                                | `200 OK`          | —                                         |
| GET    | `/tasks/{task_id}`   | Returns a single task by its `id`                                             | `200 OK`          | `404` if `task_id` doesn't exist          |
| POST   | `/tasks`             | Creates a new task from the request body (`title` required)                  | `200 OK`          | `400` if `title` is missing/empty         |
| PUT    | `/tasks/{task_id}`   | Updates `title` and/or `done` for an existing task; only provided fields change | `200 OK`        | `400` if body is empty/invalid, `404` if `task_id` doesn't exist |
| DELETE | `/tasks/{task_id}`   | Deletes a task by its `id`                                                     | `204 No Content`  | `404` if `task_id` doesn't exist          |

Curl output:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Create a new task"
}'
```


<img width="1920" height="1080" alt="Screenshot 2026-08-01 222050" src="https://github.com/user-attachments/assets/c0f883eb-7eae-4e52-875f-2f2e8e2b58c3" />
