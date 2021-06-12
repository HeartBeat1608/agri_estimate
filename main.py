#!/usr/bin/python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from model import RFR_Model
from model_types import YieldResponse, PredictionRequest

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/web", StaticFiles(directory="static"), name="static")


RanFor = RFR_Model()
RanFor.load_data()


@app.get("/")
def server_static():
    return RedirectResponse(url='/web/index.html', status_code=302)


@app.post('/get_yield', response_model=YieldResponse)
def get_result(request: PredictionRequest):
    pred = RanFor.predict(request.city, request.crop,
                          request.soil, request.area, request.season)
    return pred


@app.get('/get_categorical')
def get_categorical():
    if len(RanFor.DISTRICTS) == 0:
        RanFor.load_data()
    return {
        'districts': RanFor.DISTRICTS,
        'crops': RanFor.CROPS,
        'seasons': RanFor.SEASONS,
        'soils': RanFor.SOILS,
    }


@app.get('/ping')
def test():
    return {'ping': "All Working"}
