@Override
  public List<RecentJobPostingsBaseDto> findNDistinctLatestVacanciesFromCompanies(
      int amount) {
    // build aggregation
    final TermsAggregationBuilder aggregationBuilder =
        AggregationBuilders.terms("unique_ids").field("companyId.keyword").size(amount);
    NativeSearchQuery nsq = new NativeSearchQueryBuilder().withQuery(null)
        .withSourceFilter(new FetchSourceFilter(null, null)).addAggregation(aggregationBuilder).build();
    // retrieve only aggregation
    Aggregations aggregations = template.queryForPage(nsq, Vacancy.class).getAggregations();
    // process buckets
    StringTerms aggregation = aggregations.get("unique_ids");
    List<Bucket> buckets = aggregation.getBuckets();
    List<RecentJobPostingsBaseDto> result = new LinkedList<>();
    // enrich response
    for (Bucket bucket : buckets) {
      RecentJobPostingsBaseDto dto = new RecentJobPostingsBaseDto();
      dto.setActiveJobPostingsCount(new Long(bucket.getDocCount()).intValue());
      dto.setCompanyId(String.valueOf(bucket.getKey()));
      result.add(dto);
    }
    return result;
  }