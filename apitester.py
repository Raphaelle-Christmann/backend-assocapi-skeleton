from pathlib import Path

import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# -----------------
# CORS setup (it's black magic - keep as-is)
# -----------------
origins = [
    "*"  # allow all origins for simplicity (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

# -----------------
# CSV data
# -----------------
# spot the data folder
data = Path(__file__).parent.absolute() / 'data'

# load the CSV data into pandas dataframes
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

@app.get("/api/alive")
def is_alive():
    return {"message" : "Alive"}

@app.get("/api/associations")
def get_associations():
    names = associations_df["nom"].tolist()
    return(names)

@app.get("/api/evenements")
def get_evenements():
    events = evenements_df["nom"].tolist()
    return events

@app.get("/api/association/{association_name}")
def get_association_details(association_name:str):
    assoc_details = associations_df[associations_df["nom"] == association_name]
    if assoc_details.empty:
        raise HTTPException(status_code=404, detail = "Association not found")
    else:
        return assoc_details.to_dict(orient="records")[0]