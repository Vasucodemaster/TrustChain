from fastapi import APIRouter, HTTPException
import requests


router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


@router.get("/repository")
def get_repository(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unable to retrieve GitHub repository"
        )

    data = response.json()

    return {
        "source": "GitHub",
        "repository": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "open_issues": data.get("open_issues_count"),
        "language": data.get("language"),
        "url": data.get("html_url")
    }
