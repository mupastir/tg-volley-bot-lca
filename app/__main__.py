import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:bot", host="localhost", port=8443, reload=True)
