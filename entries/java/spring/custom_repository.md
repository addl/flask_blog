## Introduction

Spring Data is a collection of libraries that make it easy to work with data in Spring Framework-based applications. One of the key features of Spring Data is its support for repositories, which provide a way to interact with data sources using a consistent, simple API.

One of its big advantages is that it integrates easily with many kind of solution such as Databases(MySql, PostgreSql), caching solution(Redis) and indexing engines, for example Elasticsearch. Always providing a simple way for accessing the data source and making migrations seamless.

In this article I will walk you through the process of creating custom repositories taking Elasticsearch as data, although the same methodology works perfectly for others solutions.

## Why to implement custom repositories
When working with JPA repositories is very unlikely for you to create custom repositories unless you need to create dynamic queries based in several parameters, or using a custom mapper for your entities, in such cases you can not rely on Spring repository or annotated queries.

In the case of Elasticsearch the situation differ, since Elastic search provides a lot of different queries for searching and indexing, in this case using repositories will generate queries by default that in many cases don't fulfill the requirements. 

Imagine we have the following entity:
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
Now we want to query Elasticsearch in order to filter documents based on all its properties, we want to specify the range of `createdDate`, we also want to filter by `source` being LinkedIn, Indeed, etc. Finally, we want to search fragments of strings based on the `title` for example we want all job postings having the text **developer** inside its `title`.

As you can imagine, we will generate different types of queries like **Range query** for the dates, we could use to match the source **Terms Query** or **Match Query** or more, finally to look for substrings we will use **Wildcard Queries** or **Query String**. This is very difficult to achieve with the default repository.

## The traditional repository
Before proceeding with our custom implementation, lets take a look at a common Spring Data Elasticsearch repository:

````java
public interface JobPostingRepository
    extends ElasticsearchRepository<JobPostingEntity, String> {

  @Query("{\"bool\":{\"must\":{\"match\":{\"url.keyword\":\"?0\"}}}}")
  JobPostingEntity findByUrl(String encodeUrl);

}
````
We simply create an interface and extend `ElasticsearchRepository`. The method **findByUrl** is an example of how to define a custom method following Spring Data name conventions annotated with `@Query` class from Elasticsearch.

The above code is enough to perform CRUD operations supporting pagination and sorting as well, but we have already discussed some of its limitations

## Custom repository: Interface declaration

First, we need to define an interface and declare all the custom methods we need in our repository:

````java
public interface CustomJobPostingRepository {

  static final int EXTERNAL_JOB_POSTING_PAGE_SIZE = 2500;

  public static final String EXTERNAL_JOBPOSTING_INDEX_NAME = "external_job_posting";

  void updateProperties(Map<String, Object> values, String jobPostingId);

  Page<JobPostingEntity> search(JobPostingScrappedSearchDto searchDto, Pageable page);

  public Page<JobPostingEntity> findAllVisible(Pageable page);

  List<JobPostingEntity> findJobPostingIdsByPropertyAndValue(String fieldName, String value);

  void setVisivilityToFalseBySource(String source);

}
````

## Custom repository: Implementation
Below we are implementing a full search method, based on the properties present in a Search DTO object:

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

The method starts by creating a `BoolQueryBuilder` object, which is used to construct the search query. 

1. The method then checks the title field in the JobPostingScrappedSearchDto object, and if it is not empty, it adds a should clause to the query to look for the title.
2. It then checks the searchQuery field in the JobPostingScrappedSearchDto object, and if it is not empty, it adds a should clause to the query to support text query search using `QueryString`.
3. Then, it adds a must clause to the query to ensure that only visible job postings are returned using `MatchQuery`.
4. Then it checks the created date range, if both `fromDate` and `toDate` are not null, it adds a range query to the bool query.
5. Finally, the method uses the **template.queryForPage()** method to execute the search query and return a `Page` object containing the search results.

> Make sure the implementation name ends in `Impl`

## Extending our custom repository
Now we only need to extend our repository from the default/traditional repository we covered before:
````java
public interface JobPostingRepository
    extends ElasticsearchRepository<JobPostingEntity, String>, CustomJobPostingRepository {

  @Query("{\"bool\":{\"must\":{\"match\":{\"url.keyword\":\"?0\"}}}}")
  JobPostingEntity findByUrl(String encodeUrl);

}
````

Here is an example using the repository in a service:

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

## Conclusion
Spring Data repositories are a powerful and convenient way to work with data in Spring-based applications. They provide a consistent, simple API for performing CRUD operations and can be easily extended to add custom logic for more complex queries.

## References
[Custom Spring Data Repository](https://vladmihalcea.com/custom-spring-data-repository/)