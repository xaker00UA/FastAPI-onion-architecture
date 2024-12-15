from fastapi import APIRouter

router = APIRouter(tags=["customer"])


@router.get("/")
async def get_customer():
    return {"Hello world"}
