## Service layer
````java
public Map<Object, Long> getCountByProperty(String propertyName) {
    log.info("Counting entries by property: {}", propertyName);
    // check non-translatable property
    List<String> propertiesNames = new LinkedList<>();
    // Non JP properties
    if (propertyName.equals(CustomTrackingActivityRepository.JOB_SEEKER_ID_NAME)
        || propertyName.equals(CustomTrackingActivityRepository.JOB_POSTING_ID_NAME)) {
      propertiesNames.add(String.format("%s.keyword", propertyName));
    } else {
      // JP properties non-translatable
      if (propertyName.equals(CustomTrackingActivityRepository.JOB_POSTING_SOURCE_NAME)) {
        propertiesNames.add(String.format("%s.%s.keyword",
            CustomTrackingActivityRepository.JOB_POSTING_PROPERTY_NAME, propertyName));
      } else {
        // Translatable properties: matching (EN/AR)
        String enFieldName = String.format("%s.%s.en.keyword",
            CustomTrackingActivityRepository.JOB_POSTING_PROPERTY_NAME, propertyName);
        String arFieldName = String.format("%s.%s.ar.keyword",
            CustomTrackingActivityRepository.JOB_POSTING_PROPERTY_NAME, propertyName);
        propertiesNames.addAll(Arrays.asList(enFieldName, arFieldName));
      }
    }
    return this.trackingRepository.getCountByPropertyName(propertiesNames);
  }
````


## Custom repository
```java
@Override
  public long countEntriesWithJobPostingIds(List<String> jobpostingIds) {
    log.info("Counting entries for job Postings, size od IDs list: {}", jobpostingIds.size());
    NativeSearchQuery nativeSearchQuery =
        new NativeSearchQueryBuilder()
            .withIndices(TRACKING_ACTIVITY_INDEX_NAME).withQuery(QueryBuilders
                .termsQuery(String.format("%.keyword", JOB_POSTING_ID_NAME), jobpostingIds))
            .build();
    long count = this.template.count(nativeSearchQuery);
    log.info("Found {} total entries", count);
    return count;
  }

  @Override
  public Map<Object, Long> getCountByPropertyName(List<String> propertiesName) {
    SearchRequestBuilder srb = esClient.prepareSearch(TRACKING_ACTIVITY_INDEX_NAME);
    for (String property : propertiesName) {
      srb.addAggregation(AggregationBuilders.terms(property).field(property)
          .collectMode(SubAggCollectionMode.DEPTH_FIRST));
    }
    Map<Object, Long> result = new HashMap<>();
    log.info("Executing: {}", srb.toString());
    SearchResponse response = srb.execute().actionGet();
    Aggregations countByPropertyName = response.getAggregations();
    Map<String, Aggregation> asMap = countByPropertyName.getAsMap();
    for (Entry<String, Aggregation> entry : asMap.entrySet()) {
      if (entry.getValue() instanceof StringTerms) {
        StringTerms strTerm = (StringTerms) entry.getValue();
        for (Terms.Bucket value : strTerm.getBuckets()) {
          result.put(value.getKey(), value.getDocCount());
        }
      }
    }
    return result;
  }
```

### Ignoring source, only metadata
````java
NativeSearchQuery nsq = new NativeSearchQueryBuilder().withQuery(boolQuery)
        .withSourceFilter(new FetchSourceFilter(null, null))
        .withPageable(PageRequest.of(0, EXTERNAL_JOB_POSTING_PAGE_SIZE)).build();
````