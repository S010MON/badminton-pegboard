from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="/app/src/templates")

data = {"courts": [
            {"a": "Jeff", "b": "Tom", "c": "Dick", "d": "Harry"},
            {"a": "", "b": "", "c": "", "d": ""},
            {"a": "", "b": "", "c": "", "d": ""},
            {"a": "", "b": "", "c": "", "d": ""},
            ],
        "next": [],
        "waiting": []
        }


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("/index.html", {"request": request, "data": data})


@app.post("/player", response_class=HTMLResponse)
async def post_player(request: Request, name: str = Form(...)):
    print(data["waiting"])
    data["waiting"].append(name)
    return templates.TemplateResponse("/waiting_list.html", {"request": request, "data": data})


@app.delete("/player/{name}", response_class=HTMLResponse)
async def delete(request: Request, name: str):
    data["waiting"].remove(name)
    return ""


@app.put("/select/{name}", response_class=HTMLResponse)
async def select(request: Request, name: str):
    data["waiting"].remove(name)
    data["next"].append(name)
    return templates.TemplateResponse("/waiting_list.html", {"request": request, "data": data})


@app.put("/unselect/{name}", response_class=HTMLResponse)
async def unselect(request: Request, name: str):
    data["next"].remove(name)
    data["waiting"].append(name)
    return templates.TemplateResponse("/waiting_list.html", {"request": request, "data": data})


@app.get("/clear/{court}", response_class=HTMLResponse)
async def clear(request: Request, court: int):
    for char in ["a", "b", "c", "d"]:
        player = data["courts"][court][char]
        if player != "":
            data["waiting"].append(player)

    data["courts"][court] = {"a": "", "b": "", "c": "", "d": ""}

    response = Response()
    response.headers["HX-Redirect"] = "/"
    return response
