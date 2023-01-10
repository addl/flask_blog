## Introducción
Python es un poderoso lenguaje de programación que se usa ampliamente en el desarrollo de aplicaciones web. Uno de los marcos populares de Python para crear aplicaciones web es Flask. Flask es un marco web micro que es fácil de usar y proporciona una gran cantidad de funciones con muy poco código.

## Objetivo
En este tutorial, aprenderá paso a paso cómo crear una aplicación web simple usando Python y Flask.

## Requisitos
Antes de comenzar, asegúrese de tener los siguientes requisitos previos instalados en su sistema:

1. Python (version 3 or above)
2. Flask (you can install it using pip install flask)

## Configurar el directorio del proyecto
Primero, cree un directorio para su proyecto y navegue hasta él. Dentro del directorio del proyecto, crea un archivo llamado `app.py`. Este será el archivo principal de su aplicación web.

## Importar el módulo Flask
En el archivo `app.py`, importe el módulo Flask. Puede hacerlo agregando la siguiente línea en la parte superior del archivo:

````python
from flask import Flask
````

## Crea una instancia de la clase Flask
Después de importar el módulo Flask, cree una instancia de la clase Flask. Puede hacer esto llamando al constructor de Flask y pasando el nombre del módulo actual como argumento.

````python
app = Flask(__name__)
````

## Definir una ruta
Una ruta es una ruta URL que escucha su aplicación. Cuando un usuario visita una ruta, su aplicación ejecutará el código asociado con esa ruta.

Para definir una ruta, puede usar el decorador `@app.route`. Por ejemplo, para definir una ruta que muestre un mensaje de saludo, puede usar el siguiente código:

````python
@app.route('/')
def hello():
    return 'Hello, World!'
````

En este ejemplo, la ruta '/' mostrará el mensaje de bienvenida "¡Hola, mundo!", cuando un usuario lo visita.

## Ejecutar la aplicación
Ahora que ha definido una ruta, puede ejecutar la aplicación llamando al método de ejecución de la clase Flask. Puede hacerlo agregando el siguiente código en la parte inferior del archivo app.py:

````python
if __name__ == '__main__':
    app.run()
````

Para iniciar el servidor web, abra una ventana de terminal y navegue hasta el directorio del proyecto. Luego, ejecuta el siguiente comando:

````python
python app.py
````

Esto iniciará el servidor web y debería ver el siguiente mensaje:

````commandline
* Running on http://127.0.0.1:5000/
````

Ahora, abra un navegador web y visite [http://localhost:5000/](http://localhost:5000/). Debería ver el mensaje de saludo que definió en la ruta: 'Hello, World!'.

## Conclusión
En este tutorial, aprendió a crear una aplicación web simple con Python y Flask. Definió una ruta y creó una función simple que muestra un mensaje de saludo. Ahora puede construir sobre esta base y agregar más funciones a su aplicación.