import uvicorn


if __name__ == "__main__":
    uvicorn.run("bot:app", host="localhost", port=8443, reload=True)
