# app/run.py
import uvicorn

def main():
    uvicorn.run(
        "app.main:app",  # path to your FastAPI app
    )

if __name__ == "__main__":
    main()
