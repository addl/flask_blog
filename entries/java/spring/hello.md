## Generate Project
Go to:

[https://start.spring.io/](https://start.spring.io/)

On this page we can generate a prototype project to work with, as you can see we are creating a project using Maven and Java and for the sake of this tutorial I am entering in te group "com.myrefactor.spring":

![New Project using PyCharm](https://drive.google.com/uc?id=1RJirQozB3p6Dg1KtcnH9SsYR7K5zoKAv)

In the right panel of the page we specify the dependencies, Spring has a lot of modules, like AOP, Spring Data, etc. For this simple tutorial we only need the Web module, to add this dependency click in "ADD DEPENDENCIES" button:

![New Project using PyCharm](https://drive.google.com/uc?id=1CVdGn6L7spxTJleJ3kx0C27QY3kD0LKA)

Then, inside the search box, enter Web and select the green square suggested

![New Project using PyCharm](https://drive.google.com/uc?id=1oyWnAMRckcU8TqMWVYiNjekU-Yx6DtLp)

Finally, to generate the project, click in the button "GENERATE" at the bottom of the page. This will download a *zip* file containing our project inside, so let's extract the folder in a convenient location in your Hard Drive

## Import IntelliJ

Our next step is to open our Java project in our IDE, I am uing IntelliJ from JetBrains. So once IntelliJ is open go to File -> Open menu and browse to the folder you extracted from the zip file, and click Open, it should look like the following:

![New Project using PyCharm](https://drive.google.com/uc?id=1DmVSyQD1CO-vgipWNlMJpCVEtte0Aaeq)

As you can notice, we have a file called:
```commandline
MyprojectApplication.java
```
The class is annotated with **SpringBootApplication**, which tells Spring this is the main file to be executed when we want to run our project.

## Creating the controller

Before to create a class representing our controller, let's create a package **controllers**, because most probably you want to create more than one controller and ideally they should be placed in a package dedictaed only for controllers. After creating the package, create a class inside this package with name "HelloController", as following:
![New Project using PyCharm](https://drive.google.com/uc?id=1VLsiTn2aEbQwiuOIFQsON_jOqk1MHROm)

Now we should annotate this class with **@RestController** to indicate Spring this class will receive request from the browser:

```java
package com.myrefactor.spring.myproject.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

}
```

But now, which URLs this controller should process? to indicates URLs there are several annotations like **@RequestMapping** for general purpose or **@GetMapping** and **@PostMapping** which explicitly indicate the HTTP method used, we will use **@GetMapping** just for demonstration purposes:

```java
...
@RestController
public class HelloController {

    @GetMapping("/")
    public String sayHello(){
        return "Hello World from Spring Controller";
    }
    
}
...
```

## Running the project

Now let's run our project and confirm that our controller is working properly, right click in the file "MyprojectApplication.java" and select "Run 'MyprojectApplication'" as follow:

![New Project using PyCharm](https://drive.google.com/uc?id=1TYC8nTizHdyVtxK45V0rV4x8MiyXXDbO)

In your console should be a message similar to this one:
```commandline
2022-04-20 16:56:53.952  INFO 10188 --- [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-04-20 16:56:53.964  INFO 10188 --- [main] c.m.s.myproject.MyprojectApplication     : Started MyprojectApplication in 3.664 seconds (JVM running for 4.375)
```
If that the case, let's go to our favourite browser and type the URL: [http://127.0.0.1](http://127.0.0.1), and the result should be:

![New Project using PyCharm](https://drive.google.com/uc?id=18leaWgojc8rjeJlSPnTeRZNdLbbXh760)

Voila!
