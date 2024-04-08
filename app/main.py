from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import mlflow
import os
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# Define tu modelo de datos de entrada
class InputData(BaseModel):
    Elevation: int
    Aspect: int
    Slope: int
    Horizontal_Distance_To_Hydrology: int
    Vertical_Distance_To_Hydrology: int
    Horizontal_Distance_To_Roadways: int
    Hillshade_9am: int
    Hillshade_Noon: int
    Hillshade_3pm: int
    Horizontal_Distance_To_Fire_Points: int
    Wilderness_Area: str
    Soil_Type: str

def load_model():
    # Configura la URI de MLflow donde se guardó el modelo
    mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:1880')
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    
    # Utiliza el ID del experimento o el nombre para cargar el modelo
    client = MlflowClient()
    run_info = client.list_run_infos('0')[0] # Asumiendo que quieres el modelo más reciente
    model_uri = f"runs:/{run_info.run_id}/RandomForestClassifier"
    model = mlflow.sklearn.load_model(model_uri)
    return model

model = load_model()

def preprocess(data: InputData):
    # Convierte la entrada en un DataFrame de Pandas
    df = pd.DataFrame([data.dict()])
    
    # Realiza el preprocesamiento, incluyendo la creación de variables dummy
    df = pd.get_dummies(df, columns = ['Wilderness_Area', 'Soil_Type'], drop_first=True)
    
    # Asegúrate de que el DataFrame tenga todas las columnas esperadas por el modelo,
    # rellena con 0s donde sea necesario
    # Aquí debes asegurarte de incluir todas las columnas posibles después del one-hot encoding
    expected_columns = ['tus', 'columnas', 'esperadas', 'aquí']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
    
    return df

@app.post("/predict/")
def predict(data: InputData):
    try:
        preprocessed_data = preprocess(data)
        prediction = model.predict(preprocessed_data)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
