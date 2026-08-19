from fastapi import FastAPI

app = FastAPI(
    title="TrustChain API",
    description="AI-Powered Contribution Intelligence & Reputation Network",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "TrustChain",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
