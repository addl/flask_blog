

# From elastic search template
````java
/*@Override
  public Optional<JobPostingEntity> findByUrl(String url) {
    log.info("Retrieving by URL: {}", url);
    Criteria criteria = new Criteria("url").is(url);
    JobPostingEntity queryForObject =
        template.queryForObject(new CriteriaQuery(criteria), JobPostingEntity.class);
    return Optional.ofNullable(queryForObject);
  }*/
````