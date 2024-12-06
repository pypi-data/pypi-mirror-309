#!/bin/bash

# Run the FastAPI server with hot reloading enabled
uvicorn felafax.server.main:app --reload --host 0.0.0.0 --port 8000 --log-level info
