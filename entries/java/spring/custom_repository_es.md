## Introducción

Spring Data es una colección de bibliotecas que facilitan el trabajo con datos en aplicaciones basadas en Spring Framework. Una de las características clave de Spring Data es su soporte para repositorios, que brindan una forma de interactuar con fuentes de datos utilizando una API simple y consistente.

Una de sus ventajas significativas es que se integra fácilmente con cualquier tipo de solución, como bases de datos (MySql, PostgreSql), soluciones de almacenamiento en caché (Redis) y motores de indexación, por ejemplo, Elasticsearch. Siempre brindando una forma simple de acceder a la fuente de datos y realizar migraciones sin inconvenientes.

En este artículo, lo guiaré a través del proceso de creación de repositorios personalizados que toman Elasticsearch como datos, aunque la misma metodología funciona perfectamente para otras soluciones.

## Por qué implementar repositorios personalizados
Cuando trabaja con repositorios JPA, es muy poco probable que cree repositorios personalizados a menos que necesite crear consultas dinámicas basadas en varios parámetros, o usar un mapeador personalizado para sus entidades, en tales casos, no puede confiar en el repositorio de Spring o consultas anotadas.

En el caso de Elasticsearch, la situación es diferente, ya que Elastic search proporciona muchas consultas diferentes para buscar e indexar, en este caso, el uso de repositorios generará consultas por defecto que en muchos casos no cumplen con los requisitos.

Imagina que tenemos la siguiente entidad:
````java
@Data
@Document(indexName = "job_posting", type = "doc")
public class JobPostingEntity {

  @Id
  private String id;
  private boolean visible;
  private Date createdDate;

  private String title;
  private String url;
  private String source;

}
````
Ahora queremos consultar Elasticsearch para filtrar documentos en función de todas sus propiedades, queremos especificar el rango de `createdDate`, también queremos filtrar por `fuente` que sea LinkedIn, Indeed, etc. Finalmente, queremos buscar fragmentos de cadenas basadas en el `título`, por ejemplo, queremos que todas las ofertas de trabajo tengan el texto **desarrollador** dentro de su `título`.

Como puede imaginar, generaremos diferentes tipos de consultas como **Consulta de rango** para las fechas, que podríamos usar para hacer coincidir la fuente **Consulta de términos** o **Consulta de coincidencia** o más, finalmente, para busque subcadenas, usaremos **Consultas comodín** o **Cadena de consulta**. Esto es muy difícil de lograr con el repositorio predeterminado.

## El repositorio tradicional
Antes de continuar con nuestra implementación personalizada, echemos un vistazo a un repositorio común de Spring Data Elasticsearch:
````java
public interface JobPostingRepository
    extends ElasticsearchRepository<JobPostingEntity, String> {

  @Query("{\"bool\":{\"must\":{\"match\":{\"url.keyword\":\"?0\"}}}}")
  JobPostingEntity findByUrl(String encodeUrl);

}
````
Simplemente creamos una interfaz y extendemos `ElasticsearchRepository`. El método **findByUrl** es un ejemplo de cómo definir un método personalizado siguiendo las convenciones de nombres de Spring Data anotadas con la clase `@Query` de Elasticsearch.

El código anterior es suficiente para realizar operaciones CRUD que también admitan la paginación y la clasificación, pero ya hemos discutido algunas de sus limitaciones.

## Repositorio personalizado: Declaración de interfaz

Primero, necesitamos definir una interfaz y declarar todos los métodos personalizados que necesitamos en nuestro repositorio:

````java
public interface CustomJobPostingRepository {

  Page<JobPostingEntity> search(JobPostingScrappedSearchDto searchDto, Pageable page);

  void setVisivilityToFalseBySource(String source);

}
````

## Repositorio personalizado: Implementación
A continuación, implementamos un método de búsqueda completo, basado en las propiedades presentes en un objeto DTO:

````java
public class CustomJobPostingRepositoryImpl implements CustomJobPostingRepository {

    @Override
    public Page<JobPostingEntity> search(JobPostingSearchDto searchDto, Pageable page) {
        log.info("Searching Job Postings: {} and page: {}", searchDto.toString(), page.toString());
        BoolQueryBuilder boolQuery = new BoolQueryBuilder();
        
        /* Look for title */
        if (!StringUtils.isEmpty(searchDto.getTitle())) {
          boolQuery.should(QueryBuilders.termQuery("title", searchDto.getTitle()));
        }
        
        /** Support for text query search */
        if (!StringUtils.isEmpty(searchDto.getSearchQuery())) {
          QueryStringQueryBuilder queryStringQuery =
                  new QueryStringQueryBuilder(String.format("*%s*", searchDto.getSearchQuery()));
          queryStringQuery.analyzeWildcard(true);
          boolQuery.should(queryStringQuery);
        }
        
        /** Only visible Job Posting */
        boolQuery.must(QueryBuilders.matchQuery("visible", true));
        
        /* Created date range */
        if (searchDto.getFromDate() != null || searchDto.getToDate() != null) {
          Long fromTime = searchDto.getFromDate() != null ? searchDto.getFromDate().getTime() : null;
          Long toTime = searchDto.getToDate() != null ? searchDto.getToDate().getTime() : null;
          QueryUtil.rangeQueryFromAndTo(boolQuery, "createdDate", fromTime, toTime);
        }
        
        return template.queryForPage(
            new NativeSearchQueryBuilder().withQuery(boolQuery).withPageable(page).build(),
            JobPostingEntity.class);
    }
}
````

El método comienza creando un objeto `BoolQueryBuilder`, que se usa para construir la consulta de búsqueda.

1. Luego, el método verifica el campo de título en el objeto JobPostingScrappedSearchDto y, si no está vacío, agrega una cláusula should a la consulta para buscar el título.
2. Luego verifica el campo searchQuery en el objeto JobPostingScrappedSearchDto y, si no está vacío, agrega una cláusula should a la consulta para respaldar la búsqueda de consulta de texto usando `QueryString`.
3. Luego, agrega una cláusula obligatoria a la consulta para garantizar que solo se devuelvan las ofertas de trabajo visibles mediante `MatchQuery`.
4. Luego verifica el rango de fechas creado, si `fromDate` y `toDate` no son nulos, agrega una consulta de rango a la consulta bool.
5. Finalmente, el método utiliza el método **template.queryForPage()** para ejecutar la consulta de búsqueda y devolver un objeto `Página` que contiene los resultados de la búsqueda.

> Asegúrate de que el nombre de la implementación termine en `Impl`

## Extendiendo nuestro repositorio personalizado
Ahora solo necesitamos extender nuestro repositorio desde el repositorio predeterminado/tradicional que cubrimos antes:

````java
public interface JobPostingRepository
    extends ElasticsearchRepository<JobPostingEntity, String>, CustomJobPostingRepository {

  @Query("{\"bool\":{\"must\":{\"match\":{\"url.keyword\":\"?0\"}}}}")
  JobPostingEntity findByUrl(String encodeUrl);

}
````

Aquí hay un ejemplo usando el repositorio en un servicio:

````java
@Service
@Slf4j
public class JobPostingService {

  private JobPostingRepository jobPostingRepository;

  @Autowired
  public JobPostingService(JobPostingRepository jobPostingRepository) {
    this.jobPostingRepository = jobPostingRepository;
  }
  
  public Page<JobPostingEntity> search(JobPostingSearchDto searchDto, Pageable page) {
    log.info("Searching Job Postings: {} with page: {}", searchDto.toString(),
        page.toString());
    Page<JobPostingEntity> searchResult = this.jobPostingRepository.search(searchDto, page);    
    return searchResult;
  }

}
````

## Conclusión
Los repositorios Spring Data son una forma poderosa y conveniente de trabajar con datos en aplicaciones basadas en Spring. Proporcionan una API simple y consistente para realizar operaciones CRUD y se pueden ampliar fácilmente para agregar lógica personalizada para consultas más complejas.

## References
[Spring Data Elasticsearch](https://docs.spring.io/spring-data/elasticsearch/docs/current/reference/html/)

[Custom Spring Data Repository](https://vladmihalcea.com/custom-spring-data-repository/)