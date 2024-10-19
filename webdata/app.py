from fastapi import FastAPI

# retire the original router
# from webdata.api.v1.routes import router as v1_router
# from webdata.api.v2.routes import router as v2_router

from webdata.api.v1.events import router as v1_event_router
from webdata.api.v1.sections import router as v1_section_router
from webdata.api.v1.schedules import router as v1_schedule_router

from webdata.config import settings


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(router=v1_schedule_router, prefix="/api")
app.include_router(router=v1_section_router,   prefix="/api")
app.include_router(router=v1_event_router, prefix="/api")

#app.include_router(v2_router, prefix="/api")
#app.include_router(v1_events.router, prefix='/api')