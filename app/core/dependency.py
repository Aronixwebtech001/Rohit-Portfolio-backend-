from fastapi import Header, HTTPException, status

async def validate_user_header(user: str = Header(...)):
    """
    Dependency to check header 'user=abcd'.
    Use this only on routes that need protection.
    """
    if user != "abcd":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid user header"
        )

