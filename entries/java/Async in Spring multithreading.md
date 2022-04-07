

where to get details from Esco skills, it comes pre calculated


4 queue in rabbitMq

Adding more queue or processor


Mooaz, will migrate to have minEducationLevel and degree and certificates(list of values) certificates: { en: [], ar: []}


Check QExperience the lookups

BACKOFFICE API access to the endpoints


load all lookup, add them to cache, migrate from excel



CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes1 =
          matchingService.matchUsingQueue(entity, queue);
      CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes2 =
          matchingService.matchUsingQueue(entity, queue);
      CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes3 =
          matchingService.matchUsingQueue(entity, queue);
      CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes4 =
          matchingService.matchUsingQueue(entity, queue);

      CompletableFuture
          .allOf(matchUsingQueueRes1, matchUsingQueueRes2, matchUsingQueueRes3, matchUsingQueueRes4)
          .join();
      Instant finishData = Instant.now();
      System.out.println("Matching Time: " + Duration.between(start, finishData).toMillis() / 1000);



@Async
  public CompletableFuture<List<MatchingResponseDTO>> matchUsingQueue(
      MatchingDestinationEntity destination, Queue<MatchingSourceEntity> sources) {
    MatchingDestinationEntity destinationClone = new MatchingDestinationEntity();
    BeanUtils.copyProperties(destination, destinationClone);
    List<MatchingResponseDTO> response = new ArrayList<>();
    MatchingAlgorithmTemplate algo = algoService.findAlgorithmById(destination.getAlgorithId());
    while (!sources.isEmpty()) {
      MatchingSourceEntity source = sources.poll();
      if (source != null) {
        System.out.println(
            "ThreadL {}" + Thread.currentThread().getName() + " Source " + source.getAssetName());
        if (destinationClone.getCertificationScore() != null)
          algo.setCertificateScore(destinationClone.getCertificationScore());
        else
          algo.setCertificateScore(0.0);
        MatchingResponseDTO dto = this.match(source, destinationClone, algo);
        MatchEntity entity = new MatchEntity();
        BeanUtils.copyProperties(dto, entity);
        entity = repo.save(entity);
        BeanUtils.copyProperties(entity, dto);
        response.add(dto);
      }
    }
    return CompletableFuture.completedFuture(response);
  }
  
  
  
  

  
public MatchingDestinationEntity addVacancy(String vacancyId) {
    FindVacancyResponseDTO response = this.findVacancy(vacancyId);
    MatchingDestinationEntity entity = this.convertVacancy(response);
    MatchingDestinationEntity old = this.findEntityById(vacancyId);
    Instant start = Instant.now();
    if (old != null) {
      entity.setId(old.getId());
      long x = matchService.deleteByDestination(TakafoConstants.VACANCY_ENTITY, vacancyId);
      logger.info("removed " + x + " old matches for vacancy id " + vacancyId);
      System.out.println("removed " + x + " old matches for vacancy id " + vacancyId);
    }
    entity = destinationRepo.save(entity);

    // find EO Grade

    logger.info("Retrieving EO: " + vacancyId);
    String destinationGrade = response.getGrade();

    logger.info("EO grade: " + response.getGrade()); // if grade is null -> data issue
    String destinationStatus = response.getStatus();
    logger.info("EO status: " + response.getStatus());

    List<MatchingSourceEntity> sourcesJs = matchingService.findSourcesJS(entity);
    Queue<MatchingSourceEntity> finalSources = new ConcurrentLinkedDeque<>();
    finalSources.addAll(sourcesJs);

    /* Start processing the curresnt sources */
    CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes1 =
        matchingService.matchUsingQueue(entity, finalSources);
    CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes2 =
        matchingService.matchUsingQueue(entity, finalSources);

    List<MatchingSourceEntity> sourcesFTE = matchingService.findSourcesFTE(entity);

    if (VACANCY_STATUS_ACTIVE.compareToIgnoreCase(destinationStatus) == 0
        || VACANCY_STATUS_OPEN.compareToIgnoreCase(destinationStatus) == 0) { // first condition EO

      if (micAssets.contains(response.getCompanyName())) { // second condition EO

        if (vacancyTypes.contains(response.getOpportunityType())) { // third condition EO
          if (destinationGrade != null) {
            Integer destinationGradeIndex = takafoGrades.indexOf(destinationGrade);
            for (MatchingSourceEntity matchingSourceEntity : sourcesFTE) {
              try {
                CandidateDTO sourceCandidate =
                    candidateService.findCandidateById(matchingSourceEntity.getSourceId());
                String sourceGrade = getCandidateGrade(sourceCandidate.getAssignments());
                if (sourceGrade != null && !sourceCandidate.isEmployed()) {
                  Integer sourceGradeIndex = takafoGrades.indexOf(sourceGrade);
                  // Only MICs with grade ==, +1 or +2

                  if (micAssets.contains(sourceCandidate.getCompany())) { // first condition FTE
                    if (destinationGradeIndex == sourceGradeIndex
                        || destinationGradeIndex == (sourceGradeIndex - 1)
                        || destinationGradeIndex == (sourceGradeIndex - 2)) {
                      finalSources.add(matchingSourceEntity);
                    }

                  } else {
                    finalSources.add(matchingSourceEntity);
                  }
                }

              } catch (Exception exception) {
                logger.info("Exception thrown from Candidate Service " + exception.getMessage());
              }
            }
          }
          // else nothing if the destination Grade is null
        } else {
          // add all candidates
          finalSources.addAll(sourcesFTE);
        }
      } else {
        // add all candidates
        finalSources.addAll(sourcesFTE);
      }

      /**
       * 1. If the Vacancy of type local internship then run the local internship matching
       * 
       * 2. If the Vacancy of type global internship then run the global internship matching
       * 
       * 3. If the Vacancy of type maseeraty then run the maseeraty matching
       * 
       * 4. If the Vacancy of any other type then run the normal matching
       * 
       */

      if (entity.getOpportunityType()
          .equalsIgnoreCase(TakafoConstants.LOCAL_INTERN_SHIP_OPP_TYPE)) {
        localInternshipService.match(entity, sourcesJs);
      } else if (entity.getOpportunityType()
          .equalsIgnoreCase(TakafoConstants.GLOBAL_SHIP_OPP_TYPE)) {
        globalInternshipService.match(entity, sourcesJs);
      } else if (entity.getOpportunityType().equalsIgnoreCase(TakafoConstants.MASEERATY_OPP_TYPE)) {
        maseeratyService.match(entity, sourcesJs);
      } else {
        /* Add two more threads to the processing */
        CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes3 =
            matchingService.matchUsingQueue(entity, finalSources);
        CompletableFuture<List<MatchingResponseDTO>> matchUsingQueueRes4 =
            matchingService.matchUsingQueue(entity, finalSources);

        /* wait, till all Threads has completed */
        CompletableFuture.allOf(matchUsingQueueRes1, matchUsingQueueRes2, matchUsingQueueRes3,
            matchUsingQueueRes4).join();
        Instant finishData = Instant.now();
        System.out
            .println("Matching Time: " + Duration.between(start, finishData).toMillis() / 1000);
        // matchingService.matchUsingQueue(entity, finalSources);
      }
    }
    // else no matching should start
    return entity;
  }