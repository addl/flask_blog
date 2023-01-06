# Overview
In this entry, I will cover all types of Pointcut Designators also called PCD supported by Spring AOP.
In addition, I will provide explanations and examples for each of them.

# Introduction
In order to understand PCD we need to know the nature of Spring AOP, and its difference with AspectJ.
From Spring's documentation:
> Due to the proxy-based nature of Spring's AOP framework, protected methods are by definition not intercepted, neither for JDK proxies (where this isn't applicable) nor for CGLIB proxies (where this is technically possible but not recommendable for AOP purposes). As a consequence, any given pointcut will be matched against public methods only!

So, if your interception needs to include protected/private methods or even constructors, consider the use of Spring-driven native AspectJ weaving instead of Spring's proxy-based AOP framework. This constitutes a different mode of AOP usage with different characteristics, so be sure to make yourself familiar with weaving first before making a decision.

That being said, every method execution in Spring AOP is proxied, which means it is wrapped at runtime in order to intercept its execution. A picture says thousands of words(Source:[Spring in Action](https://www.amazon.com/Spring-Action-Sixth-Craig-Walls/dp/1617297577/ref=sr_1_4?crid=VPOOX5S4K2UT&keywords=spring+in+action+3rd+edition&qid=1653372060&sprefix=spring+in+action+3rd+edition%2Caps%2C155&sr=8-4)):

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1iHhZXbEnF45sU5ze42k5dbZV08nEr85y)


## execution
Thi PCD is used for matching method execution join points, this is the primary pointcut designator you will use when working with Spring AOP.
````java
/*
* Matches all methods inside CustomerService in disregards their signature.
* 
* First wildcard refer to any return type, the second refers to any method name and (..) to any
* parameters.
*/
@Pointcut(value = "execution(* com.myrefactor.aop.aopcookbook.service.CustomerService.*(..))")
private void pointcutAllService() {}
````

## within
Limits matching to join points within certain types (simply the execution of a method declared within a matching type when using Spring AOP).
````java
/*
* Matches all methods inside ProductService in disregards their signature.
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
It is possible also, to match types inside any package, for instance:
````java
/*
* Matches all methods inside 'service' package.
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*)")
private void pointcutAllService() {}
````

## this and target
### this
The **this** PCD limits matching to join points (the execution of methods when using Spring AOP) where the bean reference (Spring AOP proxy) is an instance of the given type.

### target
Target PCD, limits matching to join points (the execution of methods when using Spring AOP) where the target object (application object being proxied) is an instance of the given type

Spring AOP is a proxy-based system and differentiates between the proxy object itself (which is bound to this) and the target object behind the proxy (which is bound to the target).

### Spring proxy process
As we know, every Joinpoint is wrapped inside a proxy, basically, Spring can create two types of proxies, let's go through them quickly.  

* JDK-based proxy: This mechanism can only proxy by interface (so your target class needs to implement an interface, which is then also implemented by the proxy class
* CGLIB-based proxy: In this scenario Spring creates a proxy by subclassing, so the proxy becomes a subclass of the target class.

the below picture shows in more detail this process.

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1JpJ1S43O6efyMIDaykNebi2BqWxFw6lV)

Now we have a background of Spring proxy process, let's suppose we have the following Spring's component:
````java
@Service
public class ProductServiceImpl implements ProductService {
    ...
}
````
Since **ProductServiceImpl** implements an interface, Spring will create a JDK proxy, and both the proxy and the target object will be instances of *ProductService* interface. So both PCD **this** and **target** will work.

````java
/*
* Matches all methods inside inside any class which implements ProductService interface.
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
Which is equivalent to:
````java
/*
* Matches all methods inside inside any class which implements ProductService interface.
*/
@Pointcut("target(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
So, where is the difference? To understand it we need to know another AOP concept: **Introduction**.

### Introduction concept
An Introduction gives you the power of declaring additional methods or fields on behalf of a type. Spring AOP allows you to introduce new interfaces (and a corresponding implementation) to any advised object. For example, you could use an introduction to make a bean implement an IsModified interface, to simplify caching. (An introduction is known as an inter-type declaration in the AspectJ community.)  
So if in this case we make an introduction of any interface:
> Only the **this**(the proxy) will be instance of the given interface

In the above scenario, using **target would fail** to match the newly introduced interface.
In summary, **this** aims for the `proxy` while **target** aims for `the object being proxied`. In addition, if you don't use **Introduction** you should not be worried about which one to use.

## args
Limits matching to join points (the execution of methods when using Spring AOP) where the arguments are instances of the given types
Let's see an example of its usage:
````java
/*
* Matches all methods inside ProductService
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutProductService() {}

@Around(value = "pointcutProductService() && args(product)")
public Object aroundMethodReceivingProduct(ProceedingJoinPoint jp, Product product)
  throws Throwable {
    ...
}
````
We could use directly the parameter of the Joinpoint.

## @target
It limits matching to join points (the execution of methods when using Spring AOP) where the class of the executing object has an annotation of the given type
````java
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*) && @target(org.springframework.stereotype.Service)")
private void pointcutForAllServices() {}

@Around(value = "pointcutForAllServices()")
public Object aroundCustomerBean(ProceedingJoinPoint jp) throws Throwable {...}
````
> Please notice how we are using **within** to match all classes inside *service* package, but by using **@target** we explicitly target the classes annotated with *@Service*. 

## @args
Limits matching to join points (the execution of methods when using Spring AOP) where the runtime type of the actual arguments passed have annotations of the given type(s).
````java
/*
* Matches all methods inside ProductService which receive a parameter object annotated
* with @Deprecated
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService) && @args(java.lang.Deprecated)")
private void pointcutProductService() {}


@Around(value = "pointcutProductService() && args(product)")
public Object aroundMethodReceivingProduct(ProceedingJoinPoint jp, Product product) {...}
````
I have added the annotation to the product model as follows:
````java
@Deprecated
public class Product implements Serializable {..}
````

## @within
Limits matching to join points within types that have the given annotation (the execution of methods declared in types with the given annotation when using Spring AOP)
````java
@Pointcut("@within(org.springframework.stereotype.Repository)")
````
Notice that the above is equivalent to:
````java
@Pointcut("within(@org.springframework.stereotype.Repository *)")
````

## @annotation
Limits matching to join points where the subject of the Joinpoint (method being executed in Spring AOP) has the given annotation
In other words, it matches only if the method has the annotation we are given to the PCD.
````java
/*
* Matches all methods inside service package but only if it is annotated with @Auditable
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*) && @annotation(com.myrefactor.aop.aopcookbook.annotations.Auditable)")
private void pointcutCustomerServiceAuditable() {}
````

If you wonder how to implement the annotation @Auditable, here is the code:

````java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Auditable {

}
````
## Conclusion
We have covered all the PCD supported by Spring AOP and provided for each of them code examples that could be applied in real scenarios. In addition, we have covered key concepts like Proxy and Introduction.

## References
https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/aop.html#aop-pointcuts

https://howtodoinjava.com/spring-aop/aspectj-pointcut-expressions/

https://www.baeldung.com/spring-aop-pointcut-tutorial

https://www.javatpoint.com/spring-boot-aop-after-advice