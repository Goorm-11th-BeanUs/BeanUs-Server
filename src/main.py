from fastapi import FastAPI

app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/health")
async def health_check():
    return {"message": "I'm healthy"}