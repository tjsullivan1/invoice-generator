import fastapi
from starlette.templating import Jinja2Templates
from starlette.requests import Request

router = fastapi.APIRouter()

templates = Jinja2Templates("templates")


@router.get("/", include_in_schema=False)
async def index(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("home/index.html", data)


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    # TODO: Find out best way to add HTTP Status code
    return fastapi.responses.RedirectResponse(url="/static/img/favicon.ico")
