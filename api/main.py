from optimizer.Optimizer import Optimizer
from fastapi import FastAPI

app = FastAPI()

@app.get('/recommend')
async def get_recomendation(price: float):
    optimizer = Optimizer()
    parts = optimizer.run_optimalization(price)
    return parts

@app.get('/')
async def root():
    return {
        'Get recommendation': '/recommend'
    }