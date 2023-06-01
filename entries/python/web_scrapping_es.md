## poster
![Object Usage over time in JVMs](https://drive.google.com/uc?id=1W-bfYG9sTPW-FtFf-ERjldQLj5ekbJ2n)

## Introducción
Web scraping es una poderosa técnica utilizada para extraer información de sitios web. En este artículo, crearemos un fragmento de código de Python que extrae las universidades existentes en el mundo de una página web utilizando las bibliotecas lxml y requests.

## ¿Qué es LXML?
Lxml significa XML y HTML, lxml es la biblioteca rica en funciones y fácil de usar para procesar XML y HTML en el lenguaje Python.
El kit de herramientas de lxml es una implementación pythonica para las bibliotecas de C libxml2 y libxslt. Es único en el sentido de que combina la velocidad y la integridad de las funciones XML de estas bibliotecas con la simplicidad de una API nativa de Python.

## Qué es XPath
XPath viene del inglésÑ lenguaje de rutas XML. Utiliza una sintaxis que no es XML para proporcionar una forma flexible de abordar (apuntar a) diferentes partes de un documento XML. También se puede usar para probar los nodos direccionados dentro de un documento para determinar si coinciden con un patrón o no.
XPath se utiliza principalmente para navegar a través del DOM de cualquier documento XML usando XPathExpression, documentos HTML y SVG son buenos ejemplos.

## Instalación de bibliotecas

Necesitamos instalar las librerías requeridas. Ejecute el siguiente comando para instalarlos todos a la vez:

```commandline
pip install requests lxml
```
Este comando instalará las bibliotecas `requests` y `lxml`.

## El proceso de scrapping

El proceso de scrapping, en general, implica los siguientes pasos:

1. Estudiar la página HTML de la que queremos extraer información. 
2. Realización de solicitudes HTTP utilizando la biblioteca `requests` para obtener el HTML. 
3. Analizar el contenido HTML utilizando el módulo `lxml`. 
4. Extracción de datos específicos mediante expresiones `XPath`. 

Vayamos un paso a la vez.

## Estudiando el sitio web
En este post, obtendré los datos de este [sitio web] (https://webometrics.info/en/world). En esta web podemos encontrar todas las universidades del mundo. La información se muestra en una tabla con la siguiente estructura HTML:

```html
<table class="sticky-enabled tableheader-processed sticky-table">
   <thead>
      <tr>
         <th class="active"><a href="/en/world?sort=desc&amp;order=ranking" title="sort by ranking" class="active">ranking</a></th>
         <th><a href="/en/world?sort=asc&amp;order=University" title="sort by University" class="active">University</a></th>
         <th>$nbsp;</th>
         <th>Country</th>
      </tr>
   </thead>
   <tbody>
      <tr class="odd">
         <td>
            <center>1</center>
         </td>
         <td><a href="https://ror.org/03vek6s52" target="_blank">Harvard University</a></td>
         <td></td>
         <td>
            <center><img alt="bandera" src="https://webometrics.info/sites/default/files/logos/us.png"></center>
         </td>
      </tr>
      <tr>More 'tr' elements ....</tr>
   </tbody>
</table>
```

> Para ver la estructura de cualquier página en el navegador, haga clic derecho y coloque en la página un elemento de inspección seleccionado para ver la estructura del documento.

Para simplificar, extraje el fragmento HTML relevante. Al analizar el HTML podemos inferir lo siguiente:

1. Tenemos para cada universidad un elemento `tr` dentro del cuerpo de la tabla. 
2. Para cada fila (elemento `tr`) en la segunda columna de la tabla, tenemos un elemento `a` con el nombre de la universidad, en este ejemplo es `Universidad de Harvard`. 
3. Para cada fila (elemento `tr`) en la cuarta columna de la tabla, tenemos un elemento `img`, dentro de un elemento `center`, con el país donde se encuentra esta universidad. 

> Para obtener el país tenemos que leer el atributo `src` del elemento `img` y obtener el código del país, en este caso es `us`.

## Ejecutando peticiones
Después del análisis estamos listos para realizar las solicitudes:

```python
response = requests.get("https://webometrics.info/en/world")
byte_string = response.content
```

Este código envía una solicitud HTTP de tipo GET a la URL especificada utilizando la biblioteca `requests`, para ello usamos la función **get()**. La URL en este caso es "https://webometrics.info/en/world", que es la página web de destino de la que queremos recuperar datos.
Al acceder al atributo `content` del objeto `response`, accedemos al contenido de la respuesta en bytes, lo almacenamos en la variable `byte_string`. Usaremos esta respuesta sin procesar para obtener el DOM de la página HTML.

## Analizando la estructura HTML
```python
source_code = html.fromstring(byte_string)
```
El código anterior usa la función **fromstring()** del módulo `html` de la biblioteca `lxml` para analizar el contenido HTML. Convierte la cadena de bytes en un objeto de documento HTML, representado por la variable `source_code`. Este objeto de documento HTML nos permite acceder y manipular los elementos en el DOM.

## Extrayendo los datos con XPath
En este punto, tenemos una página HTML completa dentro de la variable `source_code`, por lo que estamos listos para atravesar el DOM usando XPATH. A partir de nuestro análisis tenemos que iterar a través de todas las filas de la tabla. Podríamos buscar todas las filas usando la siguiente expresión XPATH:

`"//*[@id='block-system-main']/div/table/tbody/tr"`

Aquí está el truco, NO SOY UN GURÚ EN XPATH, en su lugar utilicé el navegador Chrome para ayudarme en este asunto, al inspeccionar el HTML, puedo obtener la expresión XPATH haciendo lo siguiente:

![Spring STS Dashboard](https://drive.google.com/uc?id=1mTd8FioidaOROTFFvfmjgJJU7BYDb49Z)

Esto me dará la siguiente expresión `//*[@id="block-system-main"]/div/table[2]`, luego la modifiqué un poco para obtener `//*[@id='block -system-main']/div/table/tbody/tr`, que básicamente recupera todas las filas en el cuerpo de todas las tablas que se encuentran dentro del documento HTML.

Ahora busquemos todas las filas de la siguiente manera:
```python
rows = source_code.xpath("//*[@id='block-system-main']/div/table/tbody/tr")
```
Ahora procesaremos cada fila accediendo a sus columnas (elementos `td`) y obteniendo los datos de los nombres de las universidades y el código de país:

```python
for uni_elem in rows:
    university = uni_elem.xpath(".//td[2]/a")[0].text
    country_path = uni_elem.xpath(".//td[4]/center/img")[0].attrib['src']
    country_code = os.path.basename(country_path)[:2]
    if country_code in universities_by_country:
        the_list = universities_by_country.get(country_code)
        the_list.append(university)
        universities_by_country[country_code] = the_list
    else:
        universities_by_country[country_code] = [university]
    print(universities_by_country)
```

Aquí está la explicación completa del código anterior:

1. El código itera sobre cada elemento universitario en la lista de filas. 
2. El nombre de la universidad se obtiene seleccionando el elemento ancla `a` dentro de la segunda columna `td[2]`. 
3. El código de país se extrae del atributo `src` del elemento `img` dentro de la cuarta celda de la tabla `td[4]/center/img`. 
4. El nombre de la universidad y el código del país extraídos se almacenan en las variables university y country_code, respectivamente. 
5. Los datos se almacenan en un diccionario en el formato: 
```json
{"us": ["Harvard University", "...."]}
```

Finalmente, el diccionario se imprime en la consola de salida.

## Código de script completo
Así es como quedaría el script completo:

```python
import os.path
import requests
from lxml import html


def get_universities_data() -> {}:
    universities_by_country = {}
    response = requests.get("https://webometrics.info/en/world")
    byte_string = response.content
    source_code = html.fromstring(byte_string)
    rows = source_code.xpath("//*[@id='block-system-main']/div/table/tbody/tr")
    for uni_elem in rows:
        university = uni_elem.xpath(".//td[2]/a")[0].text
        country_path = uni_elem.xpath(".//td[4]/center/img")[0].attrib['src']
        country_code = os.path.basename(country_path)[:2]
        if country_code in universities_by_country:
            the_list = universities_by_country.get(country_code)
            the_list.append(university)
            universities_by_country[country_code] = the_list
        else:
            universities_by_country[country_code] = [university]
    print(universities_by_country)


if __name__ == "__main__":
    get_universities_data()
```

## Ejecutando el scrapper
Si tiene el código guardado en un archivo llamado `universities_scraper.py`, puede ejecutarlo usando el siguiente comando:

```commandline
python universities_scraper.py
```

Después de ejecutar el script, el resultado será similar a este:

```json
{
   "us":[
      "Harvard University",
      "Stanford University",
   ],
   "uk":[
      "University of Oxford",
   ],
   "ca":[
      "University of Toronto",
   ],
   ...
}
```
¡Felicidades! Has extraído información de un sitio web usando scrapping con Python.

## Un reto para ti
El sitio web solo enumera algunas universidades, para obtener todas las universidades, debe navegar por el sitio utilizando el parámetro de `page` de la siguiente manera:

`https://webometrics.info/en/world?page=1`

Por lo tanto, debe realizar N solicitudes al sitio con el número de página específico para obtener las universidades restantes. Practique las técnicas aprendidas en esta publicación y personalice el script para recuperar la lista completa de universidades. ¡Feliz código!

## Conclusión
En este artículo, demostramos cómo podemos aprovechar el web scraping usando la biblioteca LXML y XPath para extraer información de diferentes sitios web.
El código extrajo los datos de las universidades de una página web y los organizó por país. Después de este artículo, ahora puede comenzar su propio viaje de web scraping y recopilar datos valiosos para investigación, inteligencia comercial y otras aplicaciones.
## References

[LXML Website](https://lxml.de/)