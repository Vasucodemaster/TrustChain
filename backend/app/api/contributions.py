from fastapi import APIRouter

router = APIRouter(
    prefix="/contributions",
    tags=["Contributions"]
)


@router.get("/")
def get_contributions():
    return {
        "message": "Contribution endpoint is working"
    }
