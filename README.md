# presidio-app
A FastAPI implementation of [Microsoft Presidio](https://microsoft.github.io/presidio/).

## Why?
You can run presidio a few ways, such as via their [Streamlit application](https://huggingface.co/spaces/presidio/presidio_demo), or use it as a Python module/library. However, the Presidio [API](https://microsoft.github.io/presidio/api-docs/api-docs.html) leaves a lot to be desired and is broken up into various Flask apps. This project attempts to re-do Presidio's API deployment/packaging to allow for more unified/extensible interfaces w/ FastAPI.

## Goals
- Easy to extend
- OpenAPI spec built-in via FastAPI
- 

## To run
`poetry run uvicorn presidio_app.main:app --host 0.0.0.0 --port 8800 --reload`