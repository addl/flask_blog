## What is Internationalization?
One of the key features of Spring is its support for internationalization (I18n), which refers to the process of adapting software to support multiple languages and locales. This is increasingly common in modern systems as they pretend to reach more customers.

## Introduction
In this article we will cover how to achieve I18n in Spring applications. The project consists in setting up a Rest API supporting i18n.

## Background
In a Spring application, I18n is typically implemented using the `ResourceBundleMessageSource` class, which loads message strings from property files that are named according to the Java conventions for I18n resource bundles. For example, a message bundle for English might be stored in a file named `messages_en.properties`, while a message bundle for Spanish might be stored in a file named `messages_es.properties`.

Spring also provides support for formatting messages with placeholders, using the `MessageFormat` class. This allows you to include dynamic values in your messages, such as usernames or dates, without having to manually concatenate strings.

## Messages files
Inside the folder `src/main/resources` create a file `messages.properties` and inside the text:

````
greeting=Hello, {0}!
````

This means that our key for this message is `greeting` and the actual message will be the text Hello followed by a placeholder that can receive any value, a name for example.

Similarly to the previous one, create another inside the same folder with the name `messages_es.properties` with the text:
````
greeting=Hola, {0}!
````
Notice how this file ends with `_es` specifying that way that this file is used for Spanish language.
> When no suffix is appended to the message file like in `messages.properties`, this file is used to load messages for the default locale.

## Dependencies
````xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
````

## The controller
Let's create a Rest controller as follows:

````java
@RestController
public class GreetingsController {

  @Autowired
  private MessageSource messageSource;

  @GetMapping("/greeting")
  public String greeting(
      @RequestParam(name = "name", required = false, defaultValue = "World") String name) {
    return messageSource.getMessage("greeting", new Object[] {name},
        LocaleContextHolder.getLocale());
  }

}
````

In the above code we are injecting a bean of type `MessageSource` which allow us to access the messages stored in the messages properties through the method `getMessage`. We also declare an endpoint `/greeting` that receives a parameter `name` and return the message.

It is crucial to notice how we get the current locale by accessing `LocaleContextHolder.getLocale()` statically. Spring can follow several strategies to define the locale, process known also as `Locale Resolver`, Sessions, Cookies, HTTP Headers, etc. We will define our strategy in the following section.

## Bean configuration
Our configuration is the simplest one, we declare a Locale resolver by HTTP headers, as follows:

````java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {


  @Bean
  public LocaleResolver localeResolver() {
    AcceptHeaderLocaleResolver ahlr = new AcceptHeaderLocaleResolver();
    ahlr.setDefaultLocale(Locale.US);
    return ahlr;
  }

}
````

Above we create a bean of type `LocaleResolver`, concretely `AcceptHeaderLocaleResolver`, this implementation that simply uses the primary locale specified in the "accept-language" header of the HTTP request.

> This locale resolver does not support `setLocale`, as the client is in charge of passing the header and Spring will resolve that language.

## Testing the API
That's all you need to set up an Rest API supporting i18n, let's perform some tests. Using CURL for example:
````
curl --location --request GET "http://localhost:8080/greeting?name=MyRefactor"

Hello, MyRefactor!
````

Now using the header `Accept-Language`:

````
curl --location --request GET "http://localhost:8080/greeting?name=MyRefactor" --header "Accept-Language: es"

Hola, MyRefactor!
````

## Conclusions
In this tutorial we learned how to support i18n easily using message properties and Accpet-Language HTTP's header given the possibility to client to request resources in different languages. this can be also applied to databases or external data sources by specifying the language in which we want the information.

## References
[Guide to Internationalization in Spring Boot](https://www.baeldung.com/spring-boot-internationalization)