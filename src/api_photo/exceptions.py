from fastapi import HTTPException, status


ErrorS3 = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Server is unavailable!"
)
