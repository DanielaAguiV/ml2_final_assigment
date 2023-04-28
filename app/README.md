# Tweets Classification Model

### Instalar paquetes necesarios

Los paquetes necesarios y sus versiones se encuentran en el archivo **requirements.txt**, para instalarlos basta usar el comando

    pip<version> install -r requirements.txt


### Ejecución local

Se ha desarrollado una API usando el modulo **FastAPI**, para correrla desde una máquina local, desde consola ejecutar el siguiente comando

    python3 -m uvicorn app:app

Este comando lanza la API de flask en el localhost a través del puerto 8000, cuenta con un único endpoint, que se muestra a continuación 

- **"/predict"** de método POST, el cual espera un payload como el siguiente

        {
            "value": "Utiliza el #ConfiésateConAndina y cuéntanos esa historia que te dejó un sabor amargo, nosotros te lo      cambiamos por el sabor para disfrutar de Andina ¡Las mejores confesiones serán premiadas con Andina! No te quedes sin refrescarte"
        }