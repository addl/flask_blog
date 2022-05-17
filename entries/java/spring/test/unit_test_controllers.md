## Introduction
In this entry we will learn how to use Spring Framework and Mockito to provide test coverage to the controller layer using Rest and JSON.

## Requirements
* Maven installed
* Java 11+
* Spring Boot 2.6+
* Text editor, I am using IntelliJ

## What is JUnit?
JUnit is a unit testing open-source framework for the Java programming language. 
Java Developers use this framework to write and execute automated tests. 
In Java, there are test cases that have to be re-executed every time a new code is added. 
This is done to make sure that nothing in the code is broken.

## What is Unit Testing?
Unit testing, as the name suggests, refers to the testing of small segments of code. 
Unit tests are typically automated tests written and run by software developers to ensure that a section of an application (known as the "unit") meets its design and behaves as intended.
In this post the segment of code we are testing is the controller layer.

## Dependencies
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
````

## Setting up the project
In order to test units of a system, we should have at least a minimal system. 
Let's create an application with two endpoints to store and retrieve users

### Entity
Our entity or model class is a simple user with "name" and identifier.
````java
public class User {

  private UUID id;
  private String name;

  // getters and setter

}
````

### Service layer
We are creating a service component that will be used by our controllers.
````java
@Service
public class UserService {

  private List<User> userDataSource;

  public UserService(){
    userDataSource = new LinkedList<>();
  }

  public User addUser(User user){
    user.setId(UUID.randomUUID());
    this.userDataSource.add(user);
    return user;
  }
  
  public List<User> getAllUsers(){
    return userDataSource;
  }

}
````
In the above code, we are using in-memory data source, a simple list **userDataSource**.
We provide two methods, one to add a new user and the other to fetch all users in database(the list ;)

### Controller layer
This is the layer we are expected to test. For simplicity, we are creating a Rest controller.
````java
@RestController
public class UserController {

  @Autowired
  private UserService userService;

  @PostMapping("/add-user")
  public User submitUser(@RequestBody User newUser){
    User user = userService.addUser(newUser);
    return user;
  }

  @GetMapping("all-users")
  public List<User> getAllUsers(){
    return userService.getAllUsers();
  }

}
````
Similarly to our service, we have two methods, one to submit a User and another to retrieve all the users in database.
Notice how we are injecting "userService" as a dependency.

### Project structure
The project structure should look like this picture:  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1-LluwKGqopS1X9bFV0l37qq__M5CZPtq)


## Creating the test
Typical, unit tests are created in a separate source folder. The standard convention from the Maven and Gradle build tools is to use:

* src/main/java - for Java classes
* src/test/java - for test classes

That being said, create a class *UserControllerTest*, refer to the above picture (Project Structure), the content of the test is:
````java
class UserControllerTest {

  private MockMvc mockMvc;

  @InjectMocks
  private UserController lookupController;

  @Mock
  UserService userService;

  /**
   * @throws java.lang.Exception
   */
  @BeforeEach
  public void setUp() throws Exception {
    MockitoAnnotations.openMocks(this);
    this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
  }

  @Test
  void whenSubmitUser_thenUserIdIsGenerated() throws Exception {
    User newUser = new User();
    newUser.setName("My Refactor");

    User result = new User();
    result.setName("My Refactor");
    UUID id = UUID.randomUUID();
    result.setId(id);

    Mockito.when(userService.addUser(Mockito.any(User.class))).thenReturn(result);

    this.mockMvc
        .perform(post("/add-user").content(asJsonString(newUser)).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(notNullValue())))
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(equalTo(id.toString()))))
        .andReturn();
  }

  private static String asJsonString(final Object obj) {
    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.writeValueAsString(obj);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
````
Don't worry if right now it does not make much sense, let's go through it to understand each part.

## Understanding @InjectMocks and @Mock annotations
Basically we used these annotations to create mock-ups of the components involved in the test. 
With @InjectMocks we instantiate our controller class and inject into it the dependencies it has declared and we have annotated with @Mock
Since we annotated UserService as @Mock, we have created a bean of this type, and, due to our controller has a dependency of the same type. Mockito will inject it.

## Test preparation with @BeforeEach
Before executing a test, we create a stand-alone context by initializing the mock-ups components:
````java
@BeforeEach
public void setUp() throws Exception {
    MockitoAnnotations.openMocks(this);
    this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
}
````
> Notice that if you are using JUnit4 the annotation is @Before and instead of **openMocks** you should use **initMocks**

## Setting up behaviour

One of the advantages of using Mockito is that you can specify behavior for your mocking objects. 
````java
...
Mockito.when(userService.addUser(Mockito.any(User.class))).thenReturn(result);
...
````
In this case, we are telling the context that when the method **addUser** is invoked and its parameter is an instance of **User** class it should return a user with **id**.

> This prevents Mockito to compare the argument with the return value which sometimes leads to an empty response body from controllers in tests.

## Performing request and assertions
We have reached the most important part, the code where we perform the request to our controller and confirm that the behavior is the expected one:
````java
...
this.mockMvc
        .perform(post("/add-user").content(asJsonString(newUser)).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(notNullValue())))
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(equalTo(id.toString()))));
...
````
Summarizing:
1. First thing, we are using *mockMvc* initialized in **setUp** method to perform a request.
2. The request is POST to the URL "/add-user" and the Content-Type is APPLICATION_JSON(because our controller is REST)
3. We are using ResultActions like **andExpect** and **andDo** in combination with MockMvcResultMatchers's **status** and StatusResultMatchers's **isOk** to confirm the status is 200 OK.
4. Finally, we utilize **MockMvcResultMatchers.jsonPath** to read the JSON in the response and compare the id of the returned object.

## Running the test
To execute the test, just right-click inside the test class as follows:  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1lGoNcW3OefO6qcrTYWqhTRh8VnzUweca)

This is my favorite part, when the test bar becomes green :)

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1Z3pmbhzz8ZoVza6bDb7Ak5jOjqtGAgHv)

That's all, I hope this entry has been useful for you.

## Conclusion
In this article we have covered the simplest steps to write the simplest unit testing using Mockito and Spring Framework.