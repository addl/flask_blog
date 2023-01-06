## Introduction
In this tutorial, you will learn the fundamental concepts of Aspect-Oriented Programming(aka AOP) and create a simple application using CommandLineRunner and Spring Boot.

## Aspect Oriented Programming(AOP) terminology

AOP is arguably a programming paradigm that increases modularity by separating cross-cutting concerns inside an application. 
It achieves this by adding additional behavior to existing code without modifying it.  
I said "arguably" because many sources refer to it as a complement to Object-Oriented Programming rather than a paradigm.  
In a nutshell, the following picture should provide you with a general understanding of AOP.  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1UmEZOzg_0MwwyeFTq2dWiBP7bi5V1w3X)

### Aspect
In the above picture, the horizontal lines represent layers of an application while the vertical lines represent those operations that are "vertical" to almost any functionality, such as **logging** and **security checking**.  
These vertical operations are called **Aspect**, which is defined in AOP like:
> Modularization of a concern that cuts across multiple classes.

As you are already guessing, a set of several Aspects are defined as **Cross-Cutting Concerns**.

### Joinpoint
Another important definition a bit tricky to understand, it is defined like:
> A point during the execution of a program, such as the execution of a method or the handling of an exception.

En pocas palabras, en la imagen de arriba, un **Jointpoint** podría ser cualquier método en la capa empresarial que necesite verificar si el usuario actual tiene el rol o privilegio requerido para permitir su ejecución. En otras palabras, un Joinpoint es **donde** podemos aplicar un Aspecto.

### Pointcut
So far we have identified two concepts, one from the vertical lines(the Aspect) and another from one of our horizontal lines, the method in the business layer(Jointpoint).  
If we intercept the horizontal and the vertical lines we have a **Pointcut**, it makes sense right?  
Pointcut is:
> A Pointcut is a predicate that helps to know where tp apply an Aspect at a particular JoinPoint.

I know is getting a bit complicated. We can think of Pointcut as an expression, which in our case is.

> I want to apply the Security Aspect in any method inside the business layer that is annotated with @Secure annotation

That's all, a predicate, an expression which helps to answer the **where**. It looks better in practice. We will come to it later.

### Advice
In simple words, an **Advice** is:

> The implementation of cross-cutting concern that we are interested in applying to other modules.

Or in other words, is the action to take by an aspect at a particular Joinpoint.  
**What** do you want to do, in our case is: "verify that the user has the required privilege".
There are different types of **Advice**, they answer the question to **when**:  

* *Before*: execute the advice before the execution of the Jointpoint.
* *After return/After error*: Execute the Advice after the successful return or after throwing an exception.
* *Around*: The most powerful Advice. You can control the Before, After and return.

> In Spring, Advice is modeled as an interceptor, maintaining a chain of interceptors around the Joinpoint.

With this background let's create a simple example.

## Dependencies
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
````

## Setting up the project
Create a simple application with a Service and an Entity, we will execute it using CommandLineRunner.

### cutomer entity
A simple class with two properties "name" and "id":
````java
public class Customer {

  private String name;
  private int age;

  // getters and setters
}
````

### customer service
A component that acts as data-source as well, having two methods **addCustomer** and **getAllCustomers**.
````java
@Service
public class CustomerService {

  private static Logger LOG = LoggerFactory.getLogger(AopCookbookApplication.class);

  private List<Customer> customers;

  public CustomerService() {
    this.customers = new LinkedList<>();
  }

  public Customer addCustomer(Customer newCustomer) {
    LOG.info("Adding new customer: {}", newCustomer.getName());
    this.customers.add(newCustomer);
    return newCustomer;
  }

  public List<Customer> getAllCustomers() {
    LOG.info("Returning all customers");
    return this.customers;
  }

}
````

### the application file
This is the simplest way to run an application with Spring context, using the interface CommandLineRunner:
````java
@SpringBootApplication
public class AopCookbookApplication implements CommandLineRunner {

  private static Logger LOG = LoggerFactory.getLogger(AopCookbookApplication.class);

  @Autowired
  private CustomerService customerService;

  public static void main(String[] args) {
    SpringApplication.run(AopCookbookApplication.class, args);
  }

  @Override
  public void run(String... args) throws Exception {
    LOG.info("EXECUTING : command line runner");
    Customer newCustomer = new Customer();
    newCustomer.setName("My Refactor");
    this.customerService.addCustomer(newCustomer);
    // return customers
    List<Customer> customers = this.customerService.getAllCustomers();
    for (Customer c : customers) {
      LOG.info("Found customer: {}", c.getName());
    }
  }
}
````
Please, notice how inside the **run** method we are calling the methods **addCustomer** and **getAllCustomers()** from the CustomerService class. These two methods are our Aspects.

## Applying the advice
Let's suppose that we want to intercept all methods in CustomerService just for Logging purposes, this brings us to:  

1. The Aspect is: the Logging functionality.
2. The Jointpoint is: the service layer, specifically "CustomerService".
3. The Pointcut is: "All methods inside CustomerService".
4. The Advice is the actual code we write to fulfill the Aspect, logging when any method in CustomerService is executed
5. Finally, the type of Advice will be **Around**, for the purpose of this tutorial.

### Advice's implementation
Create a class with the name "CustomerServiceAdviceExecution", this is the content:
````java
@Component
@Aspect
public class CustomerServiceAdviceExecution {

  private static Logger LOG = LoggerFactory.getLogger(CustomerServiceAdviceExecution.class);

  /*
   * Matches all methods inside CustomerService in disregards their signature.
   * 
   * First wildcard refer to any return type, the second refers to any method name and (..) to any
   * parameters.
   */
  @Pointcut(value = "execution(* com.myrefactor.aop.aopcookbook.service.CustomerService.*(..))")
  private void pointcutAllService() {}

  @Around(value = "pointcutAllService()")
  public void aroundAllCustomerService(ProceedingJoinPoint jp) throws Throwable {
    LOG.info("Executing advise BEFORE {} method", jp.getSignature().getName());
    try {
      jp.proceed();
    } finally {
    }
    LOG.info("Executing advise AFTER {} method", jp.getSignature().getName());
  }

}
````
Important things to pay attention to are:  
* The usage of the annotation @Aspect, indicating this class is an aspect.
* We declare a Pointcut with the @Pointcut annotation. Read the comment to understand the expression.
* We annotated a method(the action to be taken) with @Around and specify the Pointcut.
* The parameter of the **aroundAllCustomerService** method is the actual Jointpont: "ProceedingJoinPoint jp".

### Executing the application
Once you run the application, the output should be similar to this one:
````commandline
c.m.a.a.AopCookbookApplication           : EXECUTING : command line runner
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise BEFORE addCustomer method
c.m.a.a.AopCookbookApplication           : Adding new customer: My Refactor
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise AFTER addCustomer method
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise BEFORE getAllCustomers method
c.m.a.a.AopCookbookApplication           : Returning all customers
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise AFTER getAllCustomers method
c.m.a.a.AopCookbookApplication           : Found customer: My Refactor
````
Voila! We are logging before and after the execution of each method inside CustomerService.

## Conclusion
We have covered the main concepts of AOP and applied this knowledge by creating a simple application that is able to intercept the execution of methods based on predicates or expressions.