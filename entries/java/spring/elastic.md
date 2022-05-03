## introduction
In this tutorial we will cover the simplest steps to integrate Spring Boot and 
Elastic search using Spring Data.

## about Elasticsearch
Elasticsearch is a distributed, RESTful search and analytics engine 
capable of addressing a growing number of use cases. It can be used also as NoSql database.

## requirements
- Java 11 installed
- Elasticsearch 7.15 (See download instructions below)
- Postman, [download](https://dl.pstmn.io/download/latest/win64)
- Your IDE, in my case IntelliJ Community

## maven dependencies
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

> Please notice that the dependency provided by Spring and the Elasticsearch you download matches in version number

These are my Elasticsearch dependencies:

![New Project using PyCharm](https://drive.google.com/uc?id=1YAt89FWXdcH91H2CIdoeg03ovU3IbXWg)

As you can see the version of the client is **7.15.2** so I downloaded the same version from [Elastic Search releases](https://www.elastic.co/downloads/past-releases#elasticsearch).

## executing elastic search server
Look for the folder where you downloaded the Elasticsearch and uncompress the file, inside "/bin" folder you can find the file:
````commandline
elasticsearch.bat
````
Execute the file, a console will open and after few seconds a successful message like the one below indicates that the server is running:
````commandline
[INFO ][o.e.i.g.DatabaseRegistry ] [DESKTOP-N55NVD4] successfully reloaded changed geoip database file
````
> In case you are using linux the file is **elasticsearch.sh**

## creating entity
Now let's create our model, the actual info we want to store in Elastcsearch, to dothat we create a Java class with all required attributes, for this tutorial the entity will be simple as:

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

Notice how we annotated it using **@Document**, this way we are specifying to Spring that this class is a document of Elasticsearch.
And this document contains two fields: **name** and **price**.
The parameter: **indexName = "product_idx"** is used to give a name to the index, which can be used to query Elasticsearch using RESTFul API clients like CURL or Postman, or even your browser, we will cover this later in this post.

## creating the repository

Spring data provides out of the box several interfaces to make easier the interaction with the data source.
In case of Elasticserach we could use ElasticSearchRepository as follows:
```java
import com.myrefactor.spring.elastic.entity.Product;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface ProductRepository extends ElasticsearchRepository<Product, String> {
}
```
We crate an interface and extends ElasticsearchRepository, we also indicated our entity class "Product" and the type of the identifiers(id) as String.

## Setting up the controller
For the purpose of this tutorial we will create a Rest controller which receives the Product and store it in elastic search.
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
Summarizing:
1. I created the controller and annotated it with **RestController** which means all data is returning in JSON format.
2. Then, I injected the Elasticsearch repository to save and retrieve data.
3. I declared a method **addProduct** to add a product to Elasticsearch.
4. Finally, I declared another method to retrieve all products from the index **getAllProducts**. 

## Executing the system

To run the system, execute this command in a console:
````commandline
mvn spring-boot:run
````
If everything went ok, you should see a message like this one:
````commandline
Tomcat started on port(s): 8080 (http) with context path ''
Started ElasticApplication in 1.533 seconds (JVM running for 1.761)
````

## Testing in the browser
To confirm that Spring is working and is connected to Elasticsearch cluster, open the following URL in your browser:

[http://localhost:8080/products](http://localhost:8080/products)

The output in the browser should be similar to this one:
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
> I formatted the JSON so that it looks prettier ;)

You can notice that "totalElements" is zero, this is expected since we haven't added any product. Let's do that.

## Testing with Postman
After installing Postman, add a new request following the next settings:  

- Method: POST 
- URL: http://localhost:8080/product
- Body:  

````json
{
    "name": "AMD CPU Ryzen 5000",
    "price": 100
}
````

After clicking the Send button, the result should be similar to mine:

![New Project using PyCharm](https://drive.google.com/uc?id=1ChtKQiQ-J4LlKX583GlnfNOKSL9We86d)

Now, lets confirm again using our browser by opening the URL: [http://localhost:8080/products](http://localhost:8080/products)

here it is the result:
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
The output is different, "totalElements" is 1 and "content" is an array of elements, containing the one we just added. This is the expected result!

## Query Elasticsearch directly
Do you remember the property "indexName" with value "product_idx", we can query directly Elasticsearch using this value, let's see a simple example:

Open your browser in this address: [http://localhost:9200/product_idx/_search](http://localhost:9200/product_idx/_search), you should see this output:

````json
{"took":1,"timed_out":false,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0},"hits":{"total":{"value":1,"relation":"eq"},"max_score":1.0,"hits":[{"_index":"product_idx","_type":"_doc","_id":"1jJ0eoABotSxVJOonJ3X","_score":1.0,"_source":{"_class":"com.myrefactor.spring.elastic.entity.Product","name":"AMD CPU Ryzen 5000","price":100.0}}]}}
````
Here, we are reaching Elasticsearch directly, without Spring. This is possible because Elasticsearch has its own API with a lot of endpoints and methods. 
We will create a separate post only for Elasticsearch API.

## Conclusion
In this post, I have covered the simplest steps to set up and test an application using Spring Boot and Elasticsearch. Let me know in the comments below if I can help you by any mean.