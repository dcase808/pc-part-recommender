# PC parts recommender API
API which recommends best computer parts in a given budget. Optimization made using linear programming with PuLP library. API build using FastAPI.

## Installation
Clone this repo
```
git clone https://github.com/dcase808/pc-part-recommender.git .
```
Install dependencies
```
pip install -r requirements.txt
```
Run API using your ASGI server of choice (e.g. uvicorn)
```
uvicorn main:app
```