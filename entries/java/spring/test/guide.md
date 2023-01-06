## Introduction

## Packaging and source code
It's a good idea to keep the test classes separate from the main source code.
Typical, unit tests are created in a separate source folder.
The standard convention from the Maven and Gradle build tools is to use:

* src/main/java - for Java classes
* src/test/java - for test classes

It is also important to identify easily the test case associated to a given class.
For instance, if we have a controller **IndexController** in the package *com.myrefactor.controllers* under "src/main/java" we should have a test case named **IndexControllerTest(s)** inside the same package *com.myrefactor.controllers* but under the "src/test/java" directory structure.

## Test case name convention
The test names must be intuitive, and users should understand the purpose of the test by reading the name.
There are several accepted approaches, more details in this [article](https://dzone.com/articles/7-popular-unit-test-naming)
One of the most popular is the proposal of Behavior-Driven Development (BDD):  

**Given_Preconditions_When_StateUnderTest_Then_ExpectedBehavior**, the idea is to break down the tests into three part such that one could come up with preconditions, state under test and expected behavior to be written in above format. 
An example:

* Given my bank account is in credit, and I made no withdrawals recently,
* When I attempt to withdraw an amount less than my card’s limit,
* Then the withdrawal should complete without errors or warnings
    ````java
    @Test
    public void givenAnEntity_whenNoIdSpecified_thenNewEntryIsCreated() {
        // test code here
    }
    ````
To go deeper on this name strategy, please have a look a this [article](https://martinfowler.com/bliki/GivenWhenThen.html) from Martin Fowler.

## Frameworks and libraries

### JUnit
We can find out there many frameworks to perform unit testing, JUnit, RestAssured, Selenium, TestNG, etc.
Almost every developer has heard about JUnit, the reason is that IDEs like Eclipse and IntelliJ support it out of the box.
Most of us are still using JUnit 4, but JUnit 5 is already released and has a lot of improvements.

### Mockito
In unit test, a test double is a replacement of a dependent component (collaborator) of the object under test.
What makes a mock object different from the others is that it uses behavior verification. It means that the mock object verifies that it (the mock object) is being used correctly by the object under test
Using the Spring Framework for Dependency Injection, mocking becomes a natural solution for unit testing. Spring Framework provides out of the box integration with Mockito.

### Hamcrest
Hamcrest is a framework for writing matcher objects allowing ‘match’ rules to be defined declaratively. 
It is the well-known framework used for unit testing in the Java ecosystem. It's bundled in JUnit and simply put, it uses existing predicates – called matcher classes – for making assertions.
Hamcrest is commonly used with JUnit and other testing frameworks for making assertions. 
Specifically, instead of using junit‘s numerous assert methods, we only use the API's single **assertThat** statement with appropriate **matchers**.

## Test case example
Let's take a look at one minimal setup for unit testing:
````java
public class LookupControllerTests {

  private MockMvc mockMvc;

  @InjectMocks
  private LookupController lookupController;

  @Mock
  LookUpService lookupService;

  /**
   * @throws java.lang.Exception
   */
  @Before
  public void setUp() throws Exception {
    MockitoAnnotations.initMocks(this);
    this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
  }

  @Test
  public void whenSubmitLookup_thenSavedEntitiesAreReturned() throws Exception {
    // prepare payload/upload data
    Lookup uploadLookup = new Lookup();
    uploadLookup.setValue("Employee");
    List<Lookup> lookups = Arrays.asList(uploadLookup);
    // prepare return data
    LookupDTO savedLookup = new LookupDTO();
    BeanUtils.copyProperties(uploadLookup, savedLookup);
    savedLookup.setId("ES-UUID");
    List<LookupDTO> response = Arrays.asList(savedLookup);
    // prepare dependencies behavior
    Mockito.when(lookupService.addLookup(Mockito.any(List.class))).thenReturn(response);
    // perform request and assert status
    String content = asJsonString(lookups);
    MvcResult mvcResult = this.mockMvc
        .perform(post("/lookup").content(content).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$[0].id").value("ES-UUID")).andReturn();
    // assert response using Hamcrest
    assertThat(mvcResult.getResponse().getContentAsByteArray(), notNullValue());
    assertThat(mvcResult.getResponse().getStatus(), equalTo(HttpStatus.OK.value()));
  }

  // helpers
  private static String asJsonString(final Object obj) {
    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.writeValueAsString(obj);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
````
Breaking down the code we have the following:  
* Annotation **@Mock** will create a mock bean "lookupService" while **@InjectMocks** will create a bean "lookupController" and inject the dependencies accordingly, in this case "lookupService".
* We indicate Mockito to load all annotations inside this test case and create a stand-alone context only containing our target component(LookupController)
    ````java
    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
    }
    ````
* Ensuring return for injected dependencies:
    ````java
    ...
    Mockito.when(lookupService.addLookup(Mockito.any(List.class))).thenReturn(response);
    ...
    ````
  Meaning that the method *addLookup* will return the object **response**. 
  > We are using **any(List.class)** to prevent comparison between parameter and returned object.

* Inside the most important segment of the code:
    ````java
    MvcResult mvcResult = this.mockMvc
        .perform(post("/lookup").content(content).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$[0].id").value("ES-UUID")).andReturn();  
    ````
  We perform a POST request, setting up the Content-Type, asserting the status, printing the response from the controller, additionally we perform some assertions using the actual JSON. Finally, we return the MvcResult.
* Finishing the test case, we use Hamcrest to make some additional assetions:
   ````java
    assertThat(mvcResult.getResponse().getContentAsByteArray(), notNullValue());
    assertThat(mvcResult.getResponse().getStatus(), equalTo(HttpStatus.OK.value()));
   ````
  While this is optional, sometimes it becomes handy given the simplicity of hamcrest assertion mechanism

## References

[https://martinfowler.com/bliki/GivenWhenThen.html](https://martinfowler.com/bliki/GivenWhenThen.html)
[https://www.baeldung.com/java-unit-testing-best-practices](https://www.baeldung.com/java-unit-testing-best-practices)
[https://springframework.guru/mocking-unit-tests-mockito/](https://springframework.guru/mocking-unit-tests-mockito/)
