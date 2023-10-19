from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="/app/src/templates")

data = {"courts": [
            {"a": "Jeff", "b": "Tom", "c": "Dick", "d": "Harry", "clear": True},
            {"a": "", "b": "", "c": "", "d": "", "clear": False},
            {"a": "", "b": "", "c": "", "d": "", "clear": False},
            {"a": "", "b": "", "c": "", "d": "", "clear": False},
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


@app.get("/promote")
async def promote(request: Request):
    free_court = 0
    for i, court in enumerate(data["courts"]):
        print(court["clear"])
        if court["clear"]:
            free_court = i
            break
        raise HTTPException(status_code=400, detail="no court free")

    next = data["next"]
    data["next"] = []
    data["courts"][free_court] = {"a": next[0],
                                  "b": next[1],
                                  "c": next[2],
                                  "d": next[3],
                                  "clear": False}

    response = Response()
    response.headers["HX-Redirect"] = "/"
    return response


@app.get("/clear/{court}", response_class=HTMLResponse)
async def clear(request: Request, court: int):
    for char in ["a", "b", "c", "d"]:
        player = data["courts"][court][char]
        if player != "":
            data["waiting"].append(player)

    data["courts"][court] = {"a": "", "b": "", "c": "", "d": "", "clear": True}

    response = Response()
    response.headers["HX-Redirect"] = "/"
    return response
