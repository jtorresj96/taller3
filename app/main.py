from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()
class PredictionInput(BaseModel):
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float

model = joblib.load("data/model.pkl")

@app.post("/predict/")
def predict_species(input_data: PredictionInput):
    features = pd.DataFrame({
        'culmen_length_mm': [input_data.culmen_length_mm],
        'culmen_depth_mm': [input_data.culmen_depth_mm],
        'flipper_length_mm': [input_data.flipper_length_mm],
        'body_mass_g': [input_data.body_mass_g]
    })
    
    prediction = model.predict(features)

    if prediction[0] == 1:
        specie = 'MALE'
    else:
        specie = 'FEMALE'
    
    return {"species_predicted": specie}
