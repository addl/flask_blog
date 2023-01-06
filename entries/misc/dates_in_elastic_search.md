https://www.elastic.co/guide/en/elasticsearch/reference/7.17/date.html
https://www.elastic.co/guide/en/elasticsearch/reference/5.5/date.html


# error
[31m[0;39m2023-01-03 17:29:19.542 [http-nio-8099-exec-1] [s:D6E0E669733B6E6D4D9F77B251C0A81C] ERROR: o.a.c.c.C.[.[.[.[dispatcherServlet]      Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is MapperParsingException[failed to parse [createdDate]]; nested: IllegalArgumentException[Invalid format: "1672759759476" is malformed at "59476"];] with root cause
[31mjava.lang.IllegalArgumentException: Invalid format: "1672759759476" is malformed at "59476"
	at org.joda.time.format.DateTimeParserBucket.doParseMillis(DateTimeParserBucket.java:187)
	at org.joda.time.format.DateTimeFormatter.parseMillis(DateTimeFormatter.java:826)
	at org.elasticsearch.index.mapper.DateFieldMapper$DateFieldType.parse(DateFieldMapper.java:240)
	at org.elasticsearch.index.mapper.DateFieldMapper.parseCreateField(DateFieldMapper.java:465)
	at org.elasticsearch.index.mapper.FieldMapper.parse(FieldMapper.java:287)
	at org.elasticsearch.index.mapper.DocumentParser.parseObjectOrField(DocumentParser.java:468)
	at org.elasticsearch.index.mapper.DocumentParser.parseValue(DocumentParser.java:591)
	at org.elasticsearch.index.mapper.DocumentParser.innerParseObject(DocumentParser.java:396)
	at org.elasticsearch.index.mapper.DocumentParser.parseObjectOrNested(DocumentParser.java:373)
	at org.elasticsearch.index.mapper.DocumentParser.internalParseDocument(DocumentParser.java:93)
	at org.elasticsearch.index.mapper.DocumentParser.parseDocument(DocumentParser.java:66)
	at org.elasticsearch.index.mapper.DocumentMapper.parse(DocumentMapper.java:277)
	at org.elasticsearch.index.shard.IndexShard.prepareIndex(IndexShard.java:530)
	at org.elasticsearch.index.shard.IndexShard.prepareIndexOnPrimary(IndexShard.java:507)
