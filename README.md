# Taller 3:  Airflow y API de predicción

## Estudiantes
- Juan David Torres Jimenez
- William David Prada Buitrago
- Ricardo Macias Bohorquez

Este repositorio contiene todos los archivos necesarios para ejecutar un entorno de Airflow y fastAPI para el taller 3 de MLOps utilizando Docker compose.

## Requisitos previos

Antes de comenzar, asegúrate de tener Docker y Docker Compose instalados en tu sistema. Si no los tienes instalados, visita [Docker](https://www.docker.com/get-started) para descargar e instalar.

## Configuración del entorno

Para configurar y ejecutar el entorno de Airflow y fastAPI, sigue estas instrucciones:

### Iniciar el entorno con Docker Compose

1. Clona este repositorio en tu máquina local.
2. Abre una terminal y navega al directorio donde clonaste el repositorio.
3. Ejecuta el siguiente comando para iniciar el entorno:

```bash
docker-compose up
```
### Iniciar el entorno Airflow

Luego puedes ingresar a Airflow con el siguiente link: [Airflow](http://localhost:8080/dags/). Allí encontrarás los tres DAGs solicitados en el taller, los nombres de estos DAGs son: clear_penguins_table, load_penguins_data y train_penguin_sex_model

El orden recomendado de ejecutar los DAGs es:

1. load_penguins_data
2. train_penguin_sex_model
3. clear_penguins_table

Después de ejecutar estos DAGs puedes usar la API 
### Ejecutar API con el modelo entrenado

Debes entrar en el siguiente link: [Inference_model](http://127.0.0.1:8000/docs) para usar la API que permita realizar inferencia al modelo entrenado. Luego hacer click en la celda que dice POST/predict/ y se desplegará la celda, debes darle click a Try out y en Example Value Schema puedes cambiar los valores predetermindos, por último dar click al boton execute y más abajo verás la predicción del modelo.