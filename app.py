from fastapi import FastAPI, Depends, Form, Request, status
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models


app = FastAPI()

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    items = db.query(models.Items).all()
    return templates.TemplateResponse("index.html.j2", {"request": request, "items": items})


@app.post("/add")
async def add_item(request: Request, item: Annotated[str, Form()], db: Annotated[Session, Depends(get_db)]):
    items = models.Items(name=item)
    db.add(items)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{item_id}")
async def edit(request: Request, item_id: int, db: Annotated[Session, Depends(get_db)]):
    items = db.query(models.Items).filter(models.Items.id == item_id).first()
    return templates.TemplateResponse("edit.html.j2", {"request": request, "items": items})


@app.post("/update/{item_id}")
async def update_item(request: Request, item_id: int, updated_name: Annotated[str, Form()], db: Annotated[Session, Depends(get_db)]):
    items = db.query(models.Items).filter(models.Items.id == item_id).first()  
    items.name = updated_name
    
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{item_id}")
async def delete_item(request: Request, item_id: int, db: Annotated[Session, Depends(get_db)]):
    items = db.query(models.Items).filter(models.Items.id == item_id).first()
    db.delete(items)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


