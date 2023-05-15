## poster
![Elastic Search custom mapping](https://drive.google.com/uc?id=1-CxwkxYJaa05bcVi8IIp2Gj5pnRmaR-q)

## Introducción
En Elasticsearch, el mapeo de propiedad o campo define cómo se deben indexar y buscar los campos en los documentos. El mapeo especifica los tipos de datos de los campos y también pueden incluir configuraciones adicionales, como si un campo debe permitir búsquedas o no, si debe analizarse o no, etc.

En este blog, aprenderemos cómo definir mapeos personalizados para nuestros índices dentro de Elasticsearch usando Spring Data Elasticsearch.

## Por qué definir asignaciones personalizadas
Al definir un mapeo personalizado, puede especificar cómo se deben indexar y buscar los campos en los documentos. De manera predeterminada, Elasticsearch mapeará automáticamente los campos en función de sus tipos de datos, pero el mapeo personalizado le brinda más control sobre cómo se indexan y buscan los campos.

Existen varias razones por las que es posible que desee especificar un mapeo personalizado en Elasticsearch:

**Tipos de datos**: puede especificar el tipo de datos para un campo, por ejemplo, un campo de fecha o un campo booleano. Esto puede ayudar a Elasticsearch a comprender mejor los datos y optimizar cómo se indexan y buscan.

**Analizadores**: puede especificar el analizador que se utilizará para un campo, por ejemplo, un analizador estándar o un analizador de palabras clave. Esto puede ayudar a Elasticsearch a comprender mejor los datos y optimizar cómo se indexan y buscan.

**Opciones de indexación**: puede especificar si un campo debe indexarse, almacenarse y buscarse. Por ejemplo, es posible que desee indexar un campo para que se pueda buscar, pero no almacenarlo para ahorrar espacio.

**Seguridad a nivel de campo**: puede usar el mapeo personalizado para definir la seguridad a nivel de campo, por ejemplo, para hacer que ciertos campos solo sean accesibles para ciertos usuarios o roles.

**Rendimiento**: la asignación personalizada se puede utilizar para optimizar el rendimiento de la indexación y la búsqueda. Por ejemplo, puede configurar la cantidad de fragmentos y réplicas para un índice o habilitar el uso de valores de documentos para los campos.

## Requisitos
1. Cartero, [descárguelo aquí] (https://dl.pstmn.io/download/latest/win64)
2. Elasticsearch [Elastic Search versión 7.15](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.0-windows-x86_64.zip).

### Dependencias de Maven
````xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
    </dependency>
</dependencies>
````

## Caso de estudio
Nuestra aplicación tiene el siguiente diagrama:

![Elastic Search Custom Mapping](https://drive.google.com/uc?id=1LOG-pE2TP-3srUHDOLpA5bpRu4NGhxla)

Los componentes principales son: 

* **Blog**: Esta entidad es nuestro modelo, representa los datos que se almacenarán en Elasticsearch.
* **BlogRepository**: Interfaz de repositorio normal de Spring Data.
* **BlogService**: El servicio donde se implementa la lógica para procesar y almacenar la información.

## Las limitaciones de las asignaciones predeterminadas
Ahora, imaginemos que tenemos nuestro índice `blog_index` poblado con dos documentos de la siguiente manera:

![Elastic Search Custom Mapping](https://drive.google.com/uc?id=1cp56efSlvU5eiEIdsK9FkPDH9lZw_TDy)

Luego busquemos los datos usando la propiedad `url`, aquí está la consulta:
````json
{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "url.keyword": "http://myrefactor.com/es/posts/primeros-pasos-con-spring-boot-y-elasticsearch"
                }
            }
        }
    }
}
````
El resultado de esta consulta es:
````json
"hits": [
    {
        "_index": "blog_index",
        "_type": "_doc",
        "_id": "7rdusIUBedjW0gxSOSTT",
        "_score": 0.2876821,
        "_source": {
            "_class": "com.myrefactor.app.entity.Blog",
            "title": "Getting started with Spring Boot and Elasticsearch",
            "description": "A place where we talk about clean code! How to improve our code skills by applying best practices and most common design patterns in order to get a high scalable code.",
            "url": "http://myrefactor.com/es/posts/primeros-pasos-con-spring-boot-y-elasticsearch"
        }
    }
]
````
Esto se espera ya que Elastic encuentra una coincidencia para la URL:
````
http://myrefactor.com/es/posts/primeros-pasos-con-spring-boot-y-elasticsearch
````

### El problema
Ahora quiero realizar la misma consulta pero usando la URL de la segunda entrada del blog:
````json
{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "url.keyword": "https://www.myrefactor.com/search?query=large+search+term&location=New+York&from_date=2022-01-01&to_date=2022-12-31&education=bachelor+university&category=information_and_technologies&experience=5+years&salary_min=75000&salary_max=100000&sort=relevance&page=1&size=20"
                }
            }
        }
    }
}
````
Y la salida es:
````json
{
  "hits": {
    "total": {
        "value": 0,
        "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
````
¡No resultados! Elastic no puede encontrar el segundo documento, ¿qué pasó?

### Comprobando el mapeo
Lo primero que haremos será comprobar el `mapping` definido para el índice 'blog_index'. Usando Postman o su navegador, vaya a [http://127.0.0.1:9200/blog_index/_mappings](http://127.0.0.1:9200/blog_index/_mappings). Esta consulta mostrará las propiedades y como se mapean, preste especial atención a la `url`:
````json
{
  "url": {
    "type": "text",
    "fields": {
        "keyword": {
            "type": "keyword",
            "ignore_above": 256
        }
    }
  }
}
````
La clave en la definición anterior es la propiedad `ignore_above`, cuyo valor es **256**. La [Documentación](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html) dice:
> Las cadenas más largas que la configuración `ignore_above` no se indexarán ni almacenarán.

Siendo más preciso:
> Indexará solo **256** caracteres de la cadena.

Podríamos intentar recuperar el documento usando otra consulta, por ejemplo:
````json
{
    "query": {
        "bool": {
            "must": {
                "match_phrase": {
                    "url": "https://www.myrefactor.com/search?query=large+search+term&location=New+York&from_date=2022-01-01&to_date=2022-12"
                }
            }
        }
    }
}
````

Y la salida es, de hecho:

````json
{
  "hits": [
    {
        "_index": "blog_index",
        "_type": "_doc",
        "_id": "77dusIUBedjW0gxSOiQY",
        "_score": 9.677635,
        "_ignored": [
            "url.keyword"
        ],
        "_source": {
            "_class": "com.myrefactor.app.entity.Blog",
            "title": "Learning Custom Mapping in Elastic Search",
            "description": "Define custom mappings instead of using the default mapping generation",
            "url": "https://www.myrefactor.com/search?query=large+search+term&location=New+York&from_date=2022-01-01&to_date=2022-12-31&education=bachelor+university&category=information_and_technologies&experience=5+years&salary_min=75000&salary_max=100000&sort=relevance&page=1&size=20",
            "createdDate": 1673702291887
        }
    }
]
}
````
Observe cómo Elastic indica que `url.keyword` se está ignorando. Entonces, para resolver este problema, debemos definir nuestro mapeo personalizado.

## Definición de mapeo personalizado

### Configuración
Tenemos que definir un bean de tipo `RestHighLevelClient` de la siguiente manera:

````java
@Configuration
public class ElasticConfig {

  @Bean
  public RestHighLevelClient esClient() {
    ClientConfiguration clientConfiguration =
        ClientConfiguration.builder().connectedTo("localhost:9200").build();
    return RestClients.create(clientConfiguration).rest();
  }
}
````

### Creando el archivo de mapeo
Dentro de la carpeta de recursos, cree un archivo, asígnele el nombre `blog_mappings.json` y dentro del archivo defina el mapeo:
````json
{
   "properties":{
      "description":{
         "type":"text",
         "fields":{
            "keyword":{
               "type":"keyword",
               "ignore_above":256
            }
         }
      },
      "title":{
         "type":"text",
         "fields":{
            "keyword":{
               "type":"keyword",
               "ignore_above":256
            }
         }
      },
      "url":{
         "type":"text",
         "fields":{
            "keyword":{
               "type":"keyword",
               "ignore_above":1024
            }
         }
      }
   }
}
````
Tenga en cuenta cómo hemos definido `"ignore_above":1024`, para que se indexen las URL grandes.

### Cambios en el servicio de blog
Luego necesitamos inyectar el cliente de Elasticsearch definido en la configuración:
````java
public class BlogService {

    @Value("classpath:blog_mappings.json")
    private Resource resourceMapping;

    @PostConstruct
    public void initializeIndex() {
        this.createIndexIfNotPresent("blog_index");
    }
    
    private void createIndexIfNotPresent(String indexName) {
        try {
          GetIndexRequest indexRequest = new GetIndexRequest();
          indexRequest.indices("blog_index");
          boolean exists = esClient.indices().exists(indexRequest, RequestOptions.DEFAULT);
          if (!exists) {
            createIndex(indexName);
          }
        } catch (InterruptedException | ExecutionException | IOException e) {
          log.error("Can not create index {}", indexName);
        }
    }

    private void createIndex(String indexName)
      throws IOException, InterruptedException, ExecutionException {
        String mapping = getResouceasString(resourceMapping);
        CreateIndexRequest indexRequest = new CreateIndexRequest(indexName);
        indexRequest.mapping("doc", mapping, XContentType.JSON);
        CreateIndexResponse createIndexResponse =
            esClient.indices().create(indexRequest, RequestOptions.DEFAULT);
        if (createIndexResponse != null && !createIndexResponse.isAcknowledged()) {
          log.error("Can not create index {}", indexName);
        }
    }

    private String getResouceasString(Resource resourceMapping) {
        try (Reader reader = new InputStreamReader(resourceMapping.getInputStream(), "utf-8")) {
          return FileCopyUtils.copyToString(reader);
        } catch (IOException e) {
          throw new UncheckedIOException(e);
        }
    }
````
Este código usa la API Java de Elasticsearch para crear un índice si aún no existe. El método principal en este código es el método **initializeIndex()**, que está anotado con `@PostConstruct`, lo que indica que debe ejecutarse automáticamente después de crear el bean.

En general, asegura que el índice `blog_index` se crea si aún no existe, usando el mapeo especificado en la variable `resourceMapping`.

## Conclusión
En conclusión, el mapeo personalizado en Elasticsearch proporciona una forma de especificar cómo se deben indexar y buscar los campos en los documentos. Es posible que las asignaciones predeterminadas proporcionadas por Elasticsearch no siempre sean adecuadas para un caso de uso particular, y la asignación personalizada permite un mayor control sobre cómo se indexan y buscan los datos.
También resolvimos nuestro caso de estudio implementando un mapeo personalizado usando Spring Data.

## Código fuente
Como de costumbre, puede descargar el código fuente asociado a este proyecto desde [My Refactor - GitHub](https://github.com/addl/my_refactor/tree/main/mr_es_spring_custom_mapping)

¡Happy code!