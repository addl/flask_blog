https://javawithloveblog.wordpress.com/2019/07/01/custom-index-mapping-in-elasticsearch-and-spring/

ver si las anotaciones funcionan
https://stackoverflow.com/questions/44230228/spring-data-elasticsearch-settings-and-mapping-config-with-annotations-not-work

el problema
Explicar la razon del problema
https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html


@PostConstruct
  public void initializeIndex() {
    this.createIndexIfNotPresent(EXTERNAL_JOBPOSTING_INDEX_NAME);
  }

private void createIndexIfNotPresent(String indexName) {
    try {
      IndicesExistsResponse exists =
          esClient.admin().indices().exists(new IndicesExistsRequest(indexName)).get();
      if (!exists.isExists()) {
        createIndex(indexName);
      }
    } catch (InterruptedException | ExecutionException | IOException e) {
      log.error("Can not create index {}", indexName);
    }
  }

  private void createIndex(String indexName)
      throws IOException, InterruptedException, ExecutionException {
    String mapping = ResourceUtils.asString(resourceMapping);
    CreateIndexRequest indexRequest = new CreateIndexRequest(indexName);
    indexRequest.mapping("doc", mapping, XContentType.JSON);
    CreateIndexResponse createIndexResponse = esClient.admin().indices().create(indexRequest).get();
    if (createIndexResponse != null && !createIndexResponse.isAcknowledged()) {
      log.error("Can not create index {}", indexName);
    }
  }

{
	"properties": {
		"availableInArabic": {
			"type": "boolean"
		},
		"availableInEnglish": {
			"type": "boolean"
		},
		"careerLevel": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"companyName": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"contractType": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"createdDate": {
			"type": "date",
			"store": true,
			"format": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
		},
		"degree": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"description": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"education": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"experience": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"gender": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"id": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"industry": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"location": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"publishedDate": {
			"type": "long"
		},
		"salary": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"sector": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"skills": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"skillsAr": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"source": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"title": {
			"properties": {
				"ar": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"en": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				}
			}
		},
		"updatedDate": {
			"type": "date",
			"store": true,
			"format": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
		},
		"url": {
			"type": "text",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 1024
				}
			}
		},
		"visible": {
			"type": "boolean"
		}
	}
}




