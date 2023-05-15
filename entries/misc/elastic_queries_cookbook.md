https://medium.com/geekculture/elastic-search-queries-hands-on-examples-fe5b2bc10c0e

@Test
    public void testSearchShouldClause() {
        // arrange
        String indexName = "myIndex";
        String field = "myField";
        String value = "myValue";
        String documentContent = "This is a document that matches the search query.";

        SearchHit<String> matchingHit = new SearchHit<>("id", documentContent, null, null);
        SearchHits<String> searchHits = new SearchHits<>(Arrays.asList(matchingHit), 1L, 1.0F);

        BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
        MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery(field, value);
        boolQueryBuilder.should(matchQueryBuilder);

        ArgumentCaptor<BoolQueryBuilder> queryBuilderCaptor = ArgumentCaptor.forClass(BoolQueryBuilder.class);

        when(elasticsearchRestTemplate.search(any(), eq(String.class), eq(IndexCoordinates.of(indexName)))).thenReturn(searchHits);

        // act
        List<String> searchResults = searchService.searchShouldClause(indexName);

        // assert
        assertEquals(Collections.singletonList(documentContent), searchResults);

        verify(elasticsearchRestTemplate).search(any(), eq(String.class), eq(IndexCoordinates.of(indexName)));
        verify(elasticsearchRestTemplate).search(queryBuilderCaptor.capture(), eq(String.class), eq(IndexCoordinates.of(indexName)));
        BoolQueryBuilder capturedQueryBuilder = queryBuilderCaptor.getValue();
        assertTrue(capturedQueryBuilder.should().get(0).getQuery() instanceof MatchQueryBuilder);
        assertEquals(field, ((MatchQueryBuilder) capturedQueryBuilder.should().get(0).getQuery()).field());
        assertEquals(value, ((MatchQueryBuilder) capturedQueryBuilder.should().get(0).getQuery()).value());
    }