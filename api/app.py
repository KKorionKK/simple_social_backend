from fastapi import FastAPI

from api.routes import api_router


# authorization_service = AuthorizationService(manager)

app = FastAPI()

# app.add_middleware(ErrorHandlingMiddleware)
# app.add_middleware(AuthorizationMiddleware, service=authorization_service)
app.include_router(api_router)
