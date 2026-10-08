from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router

from .errors import (
    create_exception_handler,
    BookNotFound,
    TagNotFound,
    TagAlreadyExist,
    UserNotFound,
    AccessTokenRequired,
    RefreshTokenRequired,
    InvalidTokenError,
    RevokedToken,
    InsufficientPermissions,
    InvalidCredentials,
    UserAlreadyExists,
)


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A rest API for a book review web access",
    version=version,
    )

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=400,
        initial_detail={
            "message": "User with this email already exists",
            "error_code": "USER_ALREADY_EXISTS"
            }
        )
)
app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=404,
        initial_detail={
            "message": "Book not found",
            "error_code": "BOOK_NOT_FOUND"
        }
    )
)
app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code=404,
        initial_detail={
            "message": "Tag not found",
            "error_code": "TAG_NOT_FOUND"
        }
    )
)
app.add_exception_handler(
    TagAlreadyExist,
    create_exception_handler(
        status_code=400,
        initial_detail={
            "message": "Tag already exists",
            "error_code": "TAG_ALREADY_EXISTS"
        }
    )
)
app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=404,
        initial_detail={
            "message": "User not found",
            "error_code": "USER_NOT_FOUND"
        }
    )
)
app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=400,
        initial_detail={
            "message": " Provide a valid Access token",
            "resolution": "Get an access token",
            "error_code": "ACCESS_TOKEN_REQUIRED"
        }
    )
)
app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=400,
        initial_detail={
            "message": " Provide a valid Refresh token",
            "resolution": "Get a refresh token",
            "error_code": "REFRESH_TOKEN_REQUIRED"
        }
    )
)
app.add_exception_handler(
    InvalidTokenError,
    create_exception_handler(
        status_code=401,
        initial_detail={
            "message": "Invalid token",
            "resolution": "Get a valid token",
            "error_code": "INVALID_TOKEN"
        }
    )
)
app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=401,
        initial_detail={
            "message": "Revoked token",
            "resolution": "Get a new token",
            "error_code": "REVOKED_TOKEN"
        }
    )
)
app.add_exception_handler(
    InsufficientPermissions,
    create_exception_handler(
        status_code=403,
        initial_detail={
            "message": "You do not have the required permissions to access this resource",
            "error_code": "INSUFFICIENT_PERMISSIONS"
        }
    )
)
app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=401,
        initial_detail={
            "message": "Invalid Email or Password",
            "error_code": "INVALID_EMAIL_OR_PASSWORD"
        }
    )
)

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Oops! An unexpected error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        },
    )

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=['tags'])