## What's thymeleaf

Thymeleaf is a modern server-side Java template engine for both web and standalone environments.
Thymeleaf's main goal is to bring elegant natural templates to your development workflow — HTML that can be correctly displayed in browsers and also work as static prototypes, allowing for stronger collaboration in development teams

## Goal

In this tutorial I will cover the simplest steps to create a Hello World web app example with Spring Boot and Thymeleaf.

## Requirements

1. JDK 8+ or OpenJDK 8+ 
2. Maven installed 3+
3. Your favorite IDE

## Dependencies

We only need two dependencies for our example, Web and Thymeleaf, so in **pom.xml** set up the dependencies as:
````commandline
...
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
...
````

## Creating the HTML page

Thymeleaf is HTML, so let's create an HTML file called: **index.html** inside templates' folder:

![New Project using PyCharm](https://drive.google.com/uc?id=1jxevIMCmWgsIOlzafY-bqiR2UvhsSWd9)

Inside the file, put the following HTML markup:

````html
<!DOCTYPE html>
<html>
   <head>
      <meta charset = "ISO-8859-1" />
      <link href = "css/styles.css" rel = "stylesheet"/>
      <title>Spring Boot Application</title>
   </head>
   <body>
      <h4>Welcome to Thymeleaf Spring Boot web application</h4>
   </body>
</html>
````

## Creating the controller

So far we have created our page, but it needs to be served by an Spring's controller, a class annotated with **@Controller** annotation, let's create one.
First, we create a package called "controllers":

![New Project using PyCharm](https://drive.google.com/uc?id=1Wwl9wVnkXCsf7hJW9qBpGHKJBtYkEORV)

Inside this package we created a class with name "IndexController.java", and append the following content:

````java
package com.myrefactor.thymeleaf.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class IndexController {

    @RequestMapping(value = "/")
    public String index() {
        return "index";
    }

}
````

Important things to notice here is the annotation **@RequestMapping**, basically we are telling Spring to map the method **index()** to the URL "/" which is the root of our server.
Another detail is that we return a String, which by default should be the name of the template or HTML file we want to show, in this method we return "index", so Spring will render the file "index.html" located inside the template folder.

## Running the project

In the terminal, inside the project's folder run:
````commandline
mvn spring-boot:run
````

If everything went ok, you should see something similar to this output:

````commandline
2022-04-23 18:46:44.311  ... Tomcat started on port(s): 8080 (http) with context path ''
2022-04-23 18:46:44.316  ... Started ThymeleafApplication in 0.876 seconds (JVM running for 1.076)
````
Which means the server is lestening in the port 8080, so let's open the browser in
[http://127.0.0.1:8080](http://127.0.0.1:8080)
The page shoud be as follow:

![New Project using PyCharm](https://drive.google.com/uc?id=18g3m3_dbWkGLBeZ51iV7H5ZZpAssnOsp)

Feel free to edit the HTML at your convenience, in another post we will discuss more Thymeleaf features.