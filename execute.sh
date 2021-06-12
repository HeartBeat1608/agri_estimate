#!/bin/bash

python -m uvicorn main:app --reload &
python -m webbrowser "http://localhost:8000/web/index.html"