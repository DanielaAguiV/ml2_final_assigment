# Tweets Classification Model

## Instalar paquetes necesarios

El manejo de versiones se hace mediante poetry, para instalar las dependencias necesarias, desde la carpeta app se debe ejecutar el comando

    poetry install


## Ejecución local

Se ha desarrollado una API usando el modulo **FastAPI**, para correrla desde una máquina local, desde consola ejecutar el siguiente comando

    python3 -m uvicorn app:app

Este comando lanza la API de flask en el localhost a través del puerto 8000, cuenta con un único endpoint, que se muestra a continuación 

- **"/predict"** de método POST, el cual espera un payload como el siguiente

        {
            "value": "Utiliza el #ConfiésateConAndina y cuéntanos esa historia que te dejó un sabor amargo, nosotros te lo      cambiamos por el sabor para disfrutar de Andina ¡Las mejores confesiones serán premiadas con Andina! No te quedes sin refrescarte"
        }

## Para obtener los modelos entrenados:

Se deben descargar de los siguientes links en la carpeta app/models sin modificar los nombres que tiene por defecto

* [Tokenizacion](https://drive.google.com/file/d/1wODiDFAL2r6HJbomedb9V-dqbrGYdIlp/view?usp=share_link)
* [Embedding](https://drive.google.com/file/d/1wWcHiRdAmvcCkd-W6Pl3udxkU_69MDXL/view?usp=share_link) 
* [Modelo](https://drive.google.com/file/d/1Acv_zwUgIjuejwo7VEYIqnty7MNKGNcC/view?usp=share_link)