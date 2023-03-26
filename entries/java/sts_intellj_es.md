## poster
![Eclipse STS vs IntelliJ](https://drive.google.com/uc?id=1CY0yzJh8O7mLvrCSi5Pwfn-NcGkG4nGZ) 

## Introduction
There are a lot of passionate discussions about Eclipse and IntelliJ. In my project I am the only one using Eclipse and in a recent debate I was the pre-historic protagonist. Are you still using Eclipse? you are a dinosaur!

It turns out I met with a colleague afterwards and the situation was kinda the same, and then another friend and the things kept going on. It was unavoidable the sense of emptiness and somehow sadness, because of Eclipse :)

I have been use Eclipse for a decade, it never let me down, so the less I could do is to try to support it, and that is the purpose of this article. As a Spring developer, I will describe some of the goodness of Eclipse and why I still prefer it over IntelliJ.

## What is STS
STS stands for Spring Tool Suite, and it is an integrated development environment (IDE) based on Eclipse that is specifically designed for developing applications using the Spring Framework. It provides a range of tools and features that make it easier for developers to create, test, and deploy Spring applications, including support for Spring Boot, Spring Cloud, and Spring Data. STS is available as a free download and is widely used by developers around the world.

## Spring Project initializer
STS provides a wizard interface for creating new Spring Boot projects. Allowing developers to select the dependencies and features they need and generates a complete project structure. 

![Spring Boot Initializer in STS](https://drive.google.com/uc?id=1UeiLZRi3hGjzuhbHy2rUCY8qqCDJ8f_Z) 

![Spring Boot Dependencies in STS](https://drive.google.com/uc?id=1zuBtnGwP89WgP8seeIQ8YwJD4i4-g2HQ) 


## Spring Boot Dashboard
On of my favorites features of STS is the dashboard,  it provides a general overview of the current Spring projects and applications in your workspace.  Including information about status(running, compiling, etc.), the type of Spring project (Boot, MVC, CLI or Spring Data), the port and more.

![Spring STS Dashboard](https://drive.google.com/uc?id=1HVWXjnYH1wFohlcNdtZT7GV0V4l3oyth) 

For microservices, you can have a "subset" and run only few of them, since the dashboard allows you to tag projects with an arbitrary number of tag. You also have the possibility of managing several profiles(filter/hide them), run/stop all of a subset of projects with one click.

### Live information of beans
The dashboard can also show live data of your Spring applications: 

![Spring STS Dashboard Beans](https://drive.google.com/uc?id=1MzouZxKB1P5HHaWWR47AiH4xpvzPerKd) 

You can see all information related to dependency injection. But here it doesn't end. STS can connect to running Spring processes to gather internal information of those running Spring processes and embed this data right in your source code editor!

![Spring STS Live Data](https://drive.google.com/uc?id=1lldiiNLYKO59vaJS5fluZo4mZmqPoudh) 

It can show data from different profiles running at the same time, it supports a lot of annotations like `ConditionalOnClass`, `ConditionalOnMissingBean`, and `Profile`, providing insightful information for each case sucha as whether the bean was found or not. In case of URL mapping annotations like `@GetMapping`, the developer can open the browser directly on this URL.

> STS 4 includes built-in support for Cloud Foundry, which allows developers to deploy and manage their Spring-based applications in the cloud.

### Live URL mappings
In case you are not sure what URL extensions your application defines, you can select the “Request Mappings” tab in the properties view. All the request mappings of the running app are listed - your self-defined ones at the top, the ones coming from libraries at the bottom of that list. 

![Spring STS Dashboard URL mapping](https://drive.google.com/uc?id=1GJ57GBPybATgraC5dv28P3dUbC5xgB9t) 

Double-clicking on the URL extension opens a browser for that extension, double-clicking on the code pointer opens the corresponding file of your project in an editor and jumps to the line that defines the request mapping. 


## Navigation
My favorite tool of STS! Modified in STS 4. All Spring annotations from the source code in the current workspace are visualized as symbols.

![Spring STS Navigator](https://drive.google.com/uc?id=1JduinocuZZle7BMQgVMP4rhzu_pHwTsA) 

It can show only the beans in current project(for which the editor is opened) or the beans defined only in the opened file, toggle the option by hitting cmd + 6 or ctrl + 6 repeatedly.

Let's summarize how the navigation boots your productivity by making you a sniper: 

* `@` shows all Spring annotations in the code. 
* `@/` shows all defined request mappings (mapped path, request method, source location). 
* `@+` shows all defined beans (bean name, bean type, source location). 
* `@>` shows all functions (prototype implementation) (see the Spring Cloud Function project). 
* `//` shows all request mappings of all running Spring Boot apps and opens a browser for the selected endpoint. 

![Spring STS Navigator URLs](https://drive.google.com/uc?id=1pvMut0cmS26oAa6rRqqzX8N3lvJI_1xw) 

> The URL navigation only works in the global 'go to symbol' view.


## Properties editor and autocompletion
It provides validation, code completions and information hovers about all Spring Boot Properties loaded as Maven/Gradle dependencies in either `.properties` or `.yml` format.

![Spring STS Property Editor](https://drive.google.com/uc?id=1Qmes12B8wo5Ivs941VewN6u3Rm9rn-wy) 

A very useful feature, since there are a lot of properties and this is more than welcome, it comes with documentation as well :) But we haven't finished. 

### Property injection
I didn't notice it before, at least with custom properties. But now I can inject properties into my beans with autocompletion. 

![Spring STS property injection with value](https://drive.google.com/uc?id=1amwNFxsP9UQudyOpOTFlIu2h6CC4vJeA) 

As you can see it provides additional information like in which property file the custom property is defined.

## Spring Data Support
As we know Spring Data repository relies on "method name conventions" to generate query based on Entities' properties. Well STS support the autocompletion of such methods: 

![Spring STS support for Spring Data](https://drive.google.com/uc?id=19tMjR-rM2nYvbOryBsf9LIf_EHnc6IlM) 

This is just an example for an entity(Student) having `name` and `email` using the `findBy` keyword. There are many other possibilities depending on the specific requirements of your application and combining keyword indicating the type of search (e.g. "Like" for partial matches) and/or additional properties to include in the search (e.g. "And" or "Or" to add multiple properties).
````java
findByEmailLike(String emailPattern)
findByNameOrderByNameDesc(String name)
````
Notice also how the keywords are also indicated in blue, so you don't have to remember them.

> This feature was way better in STS 3, and now we have basic support thanks to a Community Member. STS4 was re-implemented and still this feature is an ongoing work. 

## Spring SpEL expressions validations
STS support basic validation of the syntax of a SpEL expression. 
![Spring STS SpEL validations](https://drive.google.com/uc?id=1_hBBw-lgFgSok274zi18IXRXe_yu7IQz) 

In contrast, IntelliJ seems to be lesser aware of this.

![IntelliJ SpEL validations](https://drive.google.com/uc?id=1670BJtwtTUQoXged_XKAOjD92PQ0AAA-) 

In general, to write SpEL expressions is error-prone and having this basic check before compile/run is a time saver.

## General features
Below there is a list of only few features I would like to mention, although there are more: 

1. `Request Annotations validations`: STS validates the usage of `@RequestMapping` where specific mapping annotations like `@GetMapping` should be used instead. I found these annotations in legacy code.

![Spring STS request mapping validation](https://drive.google.com/uc?id=1_up6LAOlLe4GfAC_a-j8UgTdD33ql3ft) 

2. `Add starters on the fly`: Not all profiles have the same dependencies, for example `test` might have `dev-tools` while in `staging` is missing. So if I want to execute `staging` with `dev-tool` or another dependency I could do that directly from the Spring menu. 

![Spring STS starters](https://drive.google.com/uc?id=1KucMLPAcDic99iingimShAmGtyK8w7a-) 

3. `Integration with docker`: Spring Boot 2.3 introduced direct support for creating OCI container images when building Spring Boot projects. This support is now integrated in the Spring Boot Dashboard in the Spring Tools 4 for Eclipse. 

![Spring STS Docker support](https://drive.google.com/uc?id=1DFRJVS5ICa7hg0A8bDL134z9W2p-Nxwg) 

4. `Integration with Cloud Foundry`: Cloud Foundry provides a simple and scalable way to deploy and manage applications in a variety of cloud environments. 
> Cloud Foundry was developed by Pivotal Software, which is now a part of VMware.


## Personal usage
In this section I just want to highlight two plugins I use on my everyday tasks, Sonarlint and PlantUML.

### Sonarlint
SonarLint highlights gugs and security vulnerabilities as you write code, with clear guidance so you can fix them and actually improve your coding skills.

I have the plugin installed in both IDEs, Eclipse and IntelliJ, and this is what I have found:
Eclipse:
![Eclipse Sonarlint](https://drive.google.com/uc?id=1jvj60PQrev5oHUeDPCsn_Mt3L88eaZb2) 

IntelliJ:
![IntelliJ Sonarlint](https://drive.google.com/uc?id=1DtFky3yYz2O74YUJwfLugKLK7wFbubL8) 

The main difference in that Eclipse highlight the error right in the code where the issue is, while IntelliJ has them inside the window for Sonarlint.
This might appears to be minor, but in my case when I focus on solving a task is very easier for me to forget to open a window just to see if there are some suggestion to improve my code.

> I am not sure why this happens, it might be related to IDE architecture, but for me is a fact.

As a plus, the sonarlint in Eclipse can connect also to Cloud server or intranet sonar qube server. 

![Eclipse Sonarlint integration](https://drive.google.com/uc?id=1y8k7Rvw5CvWf5KI-Z73OhWPUU4BdsmbZ) 

## PlantUml
PlantUML is an open-source tool allowing users to create any sort of diagrams(Sequence, Use case, Class, Activity, etc). Particularly I use it for blog entries, wiki pages and reverse engineering when a picture says a thousand lines of code like component interaction.

After installing the plugin in IntelliJ, I noticed the following.
IntelliJ
![IntelliJ and PlantUML](https://drive.google.com/uc?id=1dRCtwpBwd_tHAuUkymh5abGpbPkgwQpr) 

And I became immediately disappointed, it is not interactive and requires a lot of user input, not productive at all. In addition, the diagram generator doesn't generate picture!, it creates a text-form PlantUml code, to be visualized in the plugin.

In contrast, PlantUml in Eclipse looks like this

![Eclipse and PLantUML](https://drive.google.com/uc?id=1hMDh2Sf4uBPoubYxm1LS2MCva2oTy1sV) 

I think I don't have to explain how useful is this for a developer, as you can have a big picture of your application. But the charm doesn't end here, you can select a simple file, package or root project folder(like in the picture) and it will automatically update the picture.

PlantUML can read PlantUML code from the comments,as bellow:
````java
/*
 @startuml

interface Shape {
  +draw(): void
}

class Circle implements Shape {
  +draw(): void
}

...

@enduml
 */
public class Main {

  public static void main(String[] args) {
    ...
  }

}
````
In case you are not fully familiar with PlantUML syntax you can copy the text from the generated picture and make adjustments and then use it as the code above (see in the picture above the contextual menu "Copy source").

## More subjective facts
No one pick IDEs because of Memory efficiency or CPU usage...well I do. I remember I coded in `vim` when I was working as FE developer in [openblender.io](https://openblender.io/#/welcome). It turns out I have good news for Eclipse lovers.

There is an interesting [study](https://dzone.com/articles/memory-efficient-ide-eclipse-or-intellij) where both IDEs where compared. The result of this study was:

![Eclipse and IntelliJ memory stats](https://drive.google.com/uc?id=13-miVVvibwt9v8rG338249CiiDwEwk12) 


### Memory
 Eclipse IDE was creating objects at the rate of **2.41 MB/sec**, whereas IntelliJ was creating objects are the rate of **69.65 MB/sec** (which is **29x more than Eclipse**). For the entire run, Eclipse only created 15.19 GB, where IntelliJ created 430.2 GB of objects. Since more objects were created, CPU consumption was also higher when using the IntelliJ IDE.

### CPU
CPU time is the total amount of time an application spends in garbage collection. It’s basically the sum of `User` time and `Sys` time.

The time Eclipse used for GC:
![Eclipse CPU stats](https://drive.google.com/uc?id=1laLVrQBBGajCIjQzHGQf_Os0ZqUX6Af7) 

While the time for IntelliJ was:
![IntelliJ CPU stats](https://drive.google.com/uc?id=1esAE0Q7jibtgKqdoWzevLyG0er7mpCVR) 

The difference is more than considerable.



## Coming improvements
The STS4 team is working to bring us the best Spring Development experience, among other things we can expect in next releases:

* Graphical representation for Spring Integration definitions #167. 
* View that displays symbol information with all your request mappings. 
* Advanced Validation for Annotations with Spring Expression Language #520. 
* Refactoring rename support for SpEL literals that references other code #521 

More than 500! It seems to me more cool stuff are incoming.

## Conclusion
Both are excellent IDEs, in my opinion IntelliJ is more polished while Eclipse is serviceable. 
I just wanted to expose some reasons than cannot be compensated with IntelliJ sugarcoating features and that doesn't make so obvious the decision of using IntelliJ over Eclipse. Happy code!


## References

[STS Wiki](https://github.com/spring-projects/sts4/wiki)

[Memory Study for Eclipse and IntelliJ](https://dzone.com/articles/memory-efficient-ide-eclipse-or-intellij)
