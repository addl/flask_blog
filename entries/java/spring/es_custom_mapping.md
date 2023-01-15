## Introduction
In Elasticsearch, mappings define how fields in documents should be indexed and searched. Mappings specify the data types of fields, and can also include additional settings such as whether a field should be searchable or not, whether it should be analyzed or not, and so on.

In this blog we will learn how to define custom mappings for our indexes inside Elasticsearch using Spring Data Elasticsearch.

## Why to define custom mappings
By defining custom mapping you can specify how fields in documents should be indexed and searched. By default, Elasticsearch will automatically map fields based on their data types, but custom mapping gives you more control over how fields are indexed and searched.

There are several reasons why you might want to specify custom mapping in Elasticsearch:

**Data types**: You can specify the data type for a field, for example, a date field or a boolean field. This can help Elasticsearch understand the data better and optimize how it is indexed and searched.

**Analyzers**: You can specify the analyzer to be used for a field, for example, a standard analyzer or a keyword analyzer. This can help Elasticsearch understand the data better and optimize how it is indexed and searched.

**Indexing options**: You can specify whether a field should be indexed, stored, and searched. For example, you might want to index a field so it can be searched, but not store it to save space.

**Field-level security**: You can use custom mapping to define field-level security, for example, to make certain fields only accessible to certain users or roles.

**Performance**: Custom mapping can be used to optimize the performance of indexing and searching. For example, you can configure the number of shards and replicas for an index, or enable the use of doc values for fields.

## Requirements
1. Postman, [download it here](https://dl.pstmn.io/download/latest/win64)
2. Elasticsearch [Elastic Search version 7.15](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.0-windows-x86_64.zip).

### Maven dependencies
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

## Case of study
Our application has the following diagram:

![Elastic Search Custom Mapping](https://drive.google.com/uc?id=1LOG-pE2TP-3srUHDOLpA5bpRu4NGhxla)

The main components are:
* **Blog entity**: Our model represents the data to be stored in Elasticsearch.
* **BlogRepository**: Spring Data normal repository interface.
* **BlogService**: The service where the logic to process and store the information is implemented.

## The limitations of default mappings
Now, let's imagine we have our index `blog_index` populated with two documents as follows:

![Elastic Search Custom Mapping](https://drive.google.com/uc?id=1cp56efSlvU5eiEIdsK9FkPDH9lZw_TDy)

Then let's fetch the data using the property `url`, here is the query:
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
The result of this query is:
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
This is expected as Elastic finds a matching for the url:
````
http://myrefactor.com/es/posts/primeros-pasos-con-spring-boot-y-elasticsearch
````

### The problem
Now I want to perform the same query but using the URL of the second blog entry:
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
And the output is:
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
Not results! Elastic is unable to find the second document, what happened?

### Checking the mappings
The first thing we will do is to check the mappings defined for the 'blog_index' index. By using Postman or your browser go to [http://127.0.0.1:9200/blog_index/_mappings](http://127.0.0.1:9200/blog_index/_mappings). This query will show the mappings, give especial attention to the `url` property's mapping:

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
The key in the above definition is `ignore_above` property, which value is **256**. The [Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html) says:
> Strings longer than the `ignore_above` setting will not be indexed or stored.

To be more precise:
> It will index only **256** characters of the string.

We could try to fetch the document using another query, for ex:
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
And the output is, indeed:
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
Notice how Elastic is indicating that `url.keyword` is being ignored. So in order to solve this issue we have to define our custom mapping.

## Defining custom mappings

### Configuration
We have to define a bean of type `RestHighLevelClient` as follows:

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

### Creating the mapping file
Inside the resource folder create a file, name it as `blog_mappings.json` and inside the content is:

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
Note how we have defined `"ignore_above":1024`, so that large URL are indexed.

### Changes in the blog service
Then we need to inject the Elasticsearch client
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
This code is using the Elasticsearch Java API to create an index if it does not already exist. The main method in this code is the **initializeIndex()** method, which is annotated with `@PostConstruct`, indicating that it should be run automatically after the bean is created.

In general, it ensures that the index `blog_index` is created if it does not already exist, using the mapping specified in the `resourceMapping` variable.

## Conclusion
In conclusion, custom mapping in Elasticsearch provides a way to specify how fields in documents should be indexed and searched. The default mappings provided by Elasticsearch may not always be suitable for a particular use case, and custom mapping allows for more control over how data is indexed and searched.

We also looked at how custom mapping can be implemented using Spring Data, to solve a specific problem that cannot be solved with default mappings.

## Sourcecode
As usual you can download the sourcecode associatted to this project from [My Refactor - GitHub](https://github.com/addl/my_refactor/tree/main/mr_es_spring_custom_mapping)

Happy Code!