## Introducci&oacute;n
En este tutorial cubriremos los pasos m&aacute;s simples para integrar Spring Boot y
Elasticsearch usando Spring Data.

## Acerca de Elasticsearch
Elasticsearch es un motor de an&aacute;lisis y b&uacute;squeda RESTful distribuido
capaz de abordar un n&uacute;mero creciente de casos de uso. Tambi&eacute;n se puede utilizar como base de datos NoSql.

## requisitos
1. Java 11 instalado
2. Elasticsearch 7.15 (Consulte las instrucciones de descarga a continuaci&oacute;n)
3. Postman, [descargar](https://dl.pstmn.io/download/latest/win64)
4. Un IDE(Entorno de Desarrollo Integrado), en mi caso IntelliJ Community

## dependencias maven
````commandline
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-web</artifactId>
</dependency>
````

> Tenga en cuenta que el n&uacute;mero de dependencia proporcionada por Spring y el Elasticsearch que descarga coincide.

Estas son mis dependencias de Elasticsearch:

![New Project using PyCharm](https://drive.google.com/uc?id=1YAt89FWXdcH91H2CIdoeg03ovU3IbXWg)

Como puede ver, la versi&oacute;n del cliente es **7.15.2** as&iacute; que descargu&eacute; la misma versi&oacute;n de [Elastic Search releases](https://www.elastic.co/downloads/past-releases#elasticsearch).

## ejecutando el servidor de Elasticsearch
Busque la carpeta donde descarg&oacute; el Elasticsearch y descomprima el archivo, dentro de la carpeta "/ bin" puede encontrar el archivo:
````commandline
elasticsearch.bat
````
Ejecute el archivo, se abrir&aacute; una consola y despu&eacute;s de unos segundos, un mensaje de &eacute;xito como el siguiente indica que el servidor se est&aacute; ejecutando:
````commandline
[INFO ][o.e.i.g.DatabaseRegistry ] [DESKTOP-N55NVD4] successfully reloaded changed geoip database file
````
> En caso de que est&eacute; utilizando Linux, el archivo es **elasticsearch.sh**

## creando el modelo o entidad
Ahora, creemos nuestro modelo, la informaci&oacute;n real que queremos almacenar en Elasticsearch, para hacerlo creamos una clase Java con todos los atributos requeridos, para este tutorial la entidad ser&aacute; tan simple como:
````java
package com.myrefactor.spring.elastic.entity;

@Document(indexName = "product_idx")
public class Product {

    @Id
    private String id;
    private String name;
    private double price;

    public Product() {
    }

    // getters and setters
}

````
Observe c&oacute;mo lo anotamos usando **@Document**, de esta forma le estamos especificando a Spring que esta clase es un documento de Elasticsearch.
Y este documento contiene dos campos: **name** y **price**.
El par&aacute;metro: **indexName = "product_idx"** se utiliza para dar un nombre al &iacute;ndice, que se puede usar para consultar Elasticsearch usando clientes de API RESTFul como CURL o Postman, o incluso su navegador, cubriremos esto m&aacute;s adelante en esta publicaci&oacute;n.

## creando el repositorio

Spring data proporciona varias interfaces listas para usar para facilitar la interacci&oacute;n con la fuente de datos.
En el caso de Elasticserach, podr&iacute;amos usar ElasticSearchRepository de la siguiente manera:
````java
import com.myrefactor.spring.elastic.entity.Product;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface ProductRepository extends ElasticsearchRepository<Product, String> {
}
````
Creamos una interfaz y extendemos ElasticsearchRepository, tambi&eacute;n indicamos nuestra clase de entidad "Product" y el tipo de los identificadores (id) como String.

## Configuraci&oacute;n del controlador

A los efectos de este tutorial, crearemos un controlador Rest que recibe el Producto y lo almacena en el cluster.
````java

import com.myrefactor.spring.elastic.entity.Product;
import com.myrefactor.spring.elastic.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductController {

    @Autowired
    private ProductRepository productRepository;

    @PostMapping("/product")
    public Product addProduct(@RequestBody Product product){
        return productRepository.save(product);
    }

    @GetMapping("/products")
    public Iterable<Product> getAllProducts(){
        return productRepository.findAll();
    }

}
````
Resumiendo:
1. Cre&eacute; el controlador y lo anot&eacute; con **RestController**, lo que significa que todos los datos se retornan en formato JSON.
2. Luego, inyect&eacute; el repositorio de Elasticsearch para guardar y recuperar datos.
3. Declar&eacute; un m&eacute;todo **addProduct** para agregar un producto a Elasticsearch.
4. Finalmente, declar&eacute; otro m&eacute;todo(**getAllProducts**) para recuperar todos los productos del cluster. 

## Ejecutando el sistema

Para ejecutar el sistema, ejecute este comando en una consola:
````commandline
mvn spring-boot:run
````
Si todo sali&oacute; bien, deber&iacute;a ver un mensaje como este:
````commandline
Tomcat started on port(s): 8080 (http) with context path ''
Started ElasticApplication in 1.533 seconds (JVM running for 1.761)
````

## Pruebas en el navegador

Para confirmar que Spring funciona y est&aacute; conectado al cl&uacute;ster de Elasticsearch, abra la siguiente URL en su navegador:
[http://localhost:8080/products](http://localhost:8080/products)

La salida en el navegador debe ser similar a esta:
````json
{
   "content": [],
   "pageable": "INSTANCE",
   "last": true,
   "totalElements": 0,
   "totalPages": 1,
   "size": 0,
   "number": 0,
   "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
   },
   "first": true,
   "numberOfElements": 0,
   "empty": true
}
````
> Formatee la JSON para que se vea m&aacute;s bonito ;)

Puede notar que "totalElements" es cero, esto es de esperar, ya que no hemos agregado ning&uacute;n producto. Manos a la obra.

## Pruebas con Postman
Despu&eacute;s de instalar Postman, agregue una nueva solicitud con la siguiente configuraci&oacute;n:

- M&eacute;todo: POST
- URL: http://localhost:8080/product
- Cuerpo:

````json
{
    "name": "AMD CPU Ryzen 5000",
    "price": 100
}
````

Despu&eacute;s de hacer clic en el bot&oacute;n "Send", el resultado deber&iacute;a ser similar al m&iacute;o:

![New Project using PyCharm](https://drive.google.com/uc?id=1ChtKQiQ-J4LlKX583GlnfNOKSL9We86d)

Ahora, confirmemos nuevamente usando su navegador abriendo la URL: [http://localhost:8080/products](http://localhost:8080/products), y el resultado es:
````json
{
   "content": [
      {
         "id": "1jJ0eoABotSxVJOonJ3X",
         "name": "AMD CPU Ryzen 5000",
         "price": 100
      }
   ],
   "pageable": {
      "sort": {
         "empty": true,
         "sorted": false,
         "unsorted": true
      },
      "offset": 0,
      "pageNumber": 0,
      "pageSize": 1,
      "unpaged": false,
      "paged": true
   },
   "last": true,
   "totalPages": 1,
   "totalElements": 1,
   "size": 1,
   "number": 0,
   "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
   },
   "first": true,
   "numberOfElements": 1,
   "empty": false
}
````
La salida es diferente, "totalElements" es 1 y "content" es una matriz de elementos que contiene el que acabamos de agregar. ¡Este es el resultado esperado!

## Query Elasticsearch directly
Recuerdas la propiedad "indexName" con valor "product_idx", podemos consultar directamente a Elasticsearch usando este valor, veamos un ejemplo simple:

Abra su navegador en esta direcci&oacute;n: [http://localhost:9200/product_idx/_search](http://localhost:9200/product_idx/_search), deber&iacute;a ver este resultado:
````json
{"took":1,"timed_out":false,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0},"hits":{"total":{"value":1,"relation":"eq"},"max_score":1.0,"hits":[{"_index":"product_idx","_type":"_doc","_id":"1jJ0eoABotSxVJOonJ3X","_score":1.0,"_source":{"_class":"com.myrefactor.spring.elastic.entity.Product","name":"AMD CPU Ryzen 5000","price":100.0}}]}}
````
Aqu&iacute;, estamos consultando directamente a Elasticsearch, sin Spring. Esto es posible porque Elasticsearch tiene su propia API. Crearemos una publicaci&oacute;n separada solo para la API de Elasticsearch.

## Conclusi&oacute;n
En este art&iacute;culo, he cubierto los pasos m&aacute;s simples para configurar y probar una aplicaci&oacute;n usando Spring Boot y Elasticsearch. Espero que te haya servido de ayuda.