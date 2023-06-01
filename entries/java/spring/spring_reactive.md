## Introduction
In the ever-evolving landscape of software development, the demand for highly scalable and responsive applications has skyrocketed. Traditional approaches to building applications often struggle to meet these demands, leading to sluggish performance and unsatisfactory user experiences. However, Spring Reactive, a paradigm introduced by the Spring Framework, offers a solution by providing a powerful and efficient way to develop responsive, non-blocking, and event-driven applications. In this article, we will delve into the concept of Spring Reactive and explore its benefits, along with a practical example to showcase its capabilities.

## Understanding Reactive Programming


## Understanding Spring Reactive
Spring Reactive is built on top of Project Reactor, an implementation of the Reactive Streams specification, which provides a programming model for asynchronous, non-blocking, and backpressure-aware stream processing. By embracing the Reactive Streams approach, Spring Reactive enables developers to build highly scalable, resilient, and responsive applications that can handle a massive number of concurrent connections.

## Benefits Reactive Programming

1. Responsiveness: With its non-blocking and event-driven nature, Spring Reactive allows applications to respond to multiple requests concurrently, without blocking threads. This leads to improved responsiveness and reduced resource consumption.
2. Scalability: Spring Reactive's ability to handle a large number of concurrent connections makes it ideal for building highly scalable applications. It efficiently utilizes system resources and can handle more workload without compromising performance.
3. Resilience: Reactive applications built with Spring Reactive are inherently more resilient. They can gracefully handle failures, thanks to features like circuit breakers, timeouts, and error handling mechanisms.
4. Functional Programming: Spring Reactive embraces functional programming principles, promoting code that is concise, modular, and easier to reason about. This leads to better maintainability and testability of the codebase.

## Reference
https://nickolasfisher.com/blog/How-to-Configure-Reactive-Netty-in-Spring-Boot-in-Depth

https://nickolasfisher.com/blog/The-Difference-Between-a-Reactive-NonBlocking-Model-and-Classic-Asynchronous-Code


https://medium.com/sysco-labs/reactive-programming-in-java-8d1f5c648012

https://spring.io/blog/2016/11/28/going-reactive-with-spring-data



https://medium.com/swlh/spring-boot-webclient-cheat-sheet-5be26cfa3e

https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html#webflux

https://developer.okta.com/blog/2018/09/24/reactive-apis-with-spring-webflux


Is the client supporting reactive or event-driven..what happens if a client make  a request to a reactive server?

Is spring reactive "override" by tmcat servevr container?

Experiment with a reactive endpoint by making a request taking a loong time and make another request, print the thread id