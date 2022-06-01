## Overview
This article will introduce the Actuator tool for monitoring and managing Spring Framework applications. You will learn how to use a few endpoints like metrics and necessary configurations like Security.

## Introduction
Spring Boot Actuator includes a number of additional features to help you monitor and manage your application when it’s pushed to production. You can choose to manage and monitor your application using HTTP endpoints, with JMX or even by remote shell (SSH or Telnet). Auditing, health and metrics gathering can be automatically applied to your application.


## Actuator Features
* **Endpoints** Actuator endpoints allow you to monitor and interact with your
  application. Spring Boot includes a number of built-in endpoints and you can also add
  your own. For example the `health` endpoint provides basic application health
  information.
* **Metrics** Spring Boot Actuator includes a metrics service with `gauge` and
  `counter` support.  A `gauge` records a single value; and a `counter` records a
  delta (an increment or decrement). Metrics for all HTTP requests are automatically
  recorded, so if you hit the `metrics` endpoint should see a sensible response.
* **Audit** Spring Boot Actuator has a flexible audit framework that will publish events
  to an `AuditService`. Once Spring Security is in play it automatically publishes
  authentication events by default. This can be very useful for reporting, and also to
  implement a lock-out policy based on authentication failures.
* **Process Monitoring** In Spring Boot Actuator you can find `ApplicationPidFileWriter`
  which creates a file containing the application PID (by default in the application
  directory with a file name of `application.pid`).

## Dependencies
The easiest way of activating actuator in Spring Boot is by adding the actuator dependency to the *pom.xml* file:
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
````

## Creating simple controller
Let's create a simple Rest controller and expose an endpoint just to see how Actuator grabs the information related to this endpoint and how we can manage it.
````java
package com.myrefactor.monitoring.demoactuator.controller;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class IndexController {

  public String showMessage(){
    return "Testing Spring Actuator";
  }

}
````

## Checking if Actuator works
Now we just need to run the application and point our browser to the URL: [http://localhost:8080/actuator](http://localhost:8080/actuator). The browser will show:
````json
{
   "_links":{
      "self":{
         "href":"http://localhost:8080/actuator",
         "templated":false
      },
      "health":{
         "href":"http://localhost:8080/actuator/health",
         "templated":false
      },
      "health-path":{
         "href":"http://localhost:8080/actuator/health/{*path}",
         "templated":true
      }
   }
}
````
As you can see we have more paths available, so for instance if you go to: [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health), the result is:
````json
{"status":"UP"}
````
Which means our application is "healthy" and running.

### Changing default endpoint
Add the following line to "application.properties":
````commandline
management.endpoints.web.base-path=/manage
````
The preceding property changes the form of the endpoint URLs from */actuator/{id}* to */manage/{id}*. 
For example, the URL health endpoint would become */manage/health*.

## Actuators Endpoints
Actuator come with a lot of endpoints, let's enable all of them to see how powerful this tool is, include the following in "application.properties":
````xml
management.endpoints.web.exposure.include=*
````
Re-run the application and go again to [http://localhost:8080/actuator](http://localhost:8080/actuator), the result now is different:
````json
{
   "_links":{
      "self":{
         "href":"http://localhost:8080/actuator",
         "templated":false
      },
      "beans":{
         "href":"http://localhost:8080/actuator/beans",
         "templated":false
      },
      "caches":{
         "href":"http://localhost:8080/actuator/caches",
         "templated":false
      },
      "caches-cache":{
         "href":"http://localhost:8080/actuator/caches/{cache}",
         "templated":true
      },
      "health":{
         "href":"http://localhost:8080/actuator/health",
         "templated":false
      },
      "health-path":{
         "href":"http://localhost:8080/actuator/health/{*path}",
         "templated":true
      },
      "info":{
         "href":"http://localhost:8080/actuator/info",
         "templated":false
      },
      "conditions":{
         "href":"http://localhost:8080/actuator/conditions",
         "templated":false
      },
      "configprops":{
         "href":"http://localhost:8080/actuator/configprops",
         "templated":false
      },
      "configprops-prefix":{
         "href":"http://localhost:8080/actuator/configprops/{prefix}",
         "templated":true
      },
      "env-toMatch":{
         "href":"http://localhost:8080/actuator/env/{toMatch}",
         "templated":true
      },
      "env":{
         "href":"http://localhost:8080/actuator/env",
         "templated":false
      },
      "loggers-name":{
         "href":"http://localhost:8080/actuator/loggers/{name}",
         "templated":true
      },
      "loggers":{
         "href":"http://localhost:8080/actuator/loggers",
         "templated":false
      },
      "heapdump":{
         "href":"http://localhost:8080/actuator/heapdump",
         "templated":false
      },
      "threaddump":{
         "href":"http://localhost:8080/actuator/threaddump",
         "templated":false
      },
      "metrics":{
         "href":"http://localhost:8080/actuator/metrics",
         "templated":false
      },
      "metrics-requiredMetricName":{
         "href":"http://localhost:8080/actuator/metrics/{requiredMetricName}",
         "templated":true
      },
      "scheduledtasks":{
         "href":"http://localhost:8080/actuator/scheduledtasks",
         "templated":false
      },
      "mappings":{
         "href":"http://localhost:8080/actuator/mappings",
         "templated":false
      }
   }
}
````
Interesting isn't it?. We could exclude some endpoints that you might not want to use, for example:
````commandline
management.endpoints.web.exposure.exclude=loggers
````
This will exclude all endpoints related to *logging*.

## Using the metrics endpoint.  
For the purpose of this tutorial, we are going to use the metrics endpoint.  
Go to: [http://localhost:8080/actuator/metrics](http://localhost:8080/actuator/metrics), you can see all the metrics actuator follows:
````json
{
  "names": [
    "application.ready.time",
    "application.started.time",
    "disk.free",
    "disk.total",
    "executor.active",
    "executor.completed",
    "executor.pool.core",
    "executor.pool.max",
    "executor.pool.size",
    "executor.queue.remaining",
    "executor.queued",
    "http.server.requests",
    "jvm.buffer.count",
    "jvm.buffer.memory.used",
    "jvm.buffer.total.capacity",
    "jvm.classes.loaded",
    "jvm.classes.unloaded",
    "jvm.gc.live.data.size",
    "jvm.gc.max.data.size",
    "jvm.gc.memory.allocated",
    "jvm.gc.memory.promoted",
    "jvm.gc.overhead",
    "jvm.gc.pause",
    "jvm.memory.committed",
    "jvm.memory.max",
    "jvm.memory.usage.after.gc",
    "jvm.memory.used",
    "jvm.threads.daemon",
    "jvm.threads.live",
    "jvm.threads.peak",
    "jvm.threads.states",
    "logback.events",
    "process.cpu.usage",
    "process.start.time",
    "process.uptime",
    "system.cpu.count",
    "system.cpu.usage",
    "tomcat.sessions.active.current",
    "tomcat.sessions.active.max",
    "tomcat.sessions.alive.max",
    "tomcat.sessions.created",
    "tomcat.sessions.expired",
    "tomcat.sessions.rejected"
  ]
}
````
Now let's create an endpoint to get the CPU usage, by combining the endpoint:
`http://localhost:8080/actuator/metrics/{requiredMetricName}` with the metric name `jvm.threads.live`. So open the browser at: [http://localhost:8080/actuator/metrics/jvm.threads.live](http://localhost:8080/actuator/metrics/jvm.threads.live), the result is
````json
{
  "name": "jvm.threads.live",
  "description": "The current number of live threads including both daemon and non-daemon threads",
  "baseUnit": "threads",
  "measurements": [
    {
      "statistic": "VALUE",
      "value": 22
    }
  ],
  "availableTags": []
}
````
Which means that my JVM has 22 live threads at this moment.

## Checking mappings
Do you remember our controller right?, we haven't seen any stat related to it. Let's check the mapping endpoint exposed by Actuator. Go to [http://localhost:8080/actuator/mappings](http://localhost:8080/actuator/mappings), there will be a lot of info, but our endpoint will be there: 
````json
...
{
  "handler": "com.myrefactor.monitoring.demoactuator.controller.IndexController#showMessage()",
  "predicate": "{GET [/say-hello-actuator]}",
  "details": {
    "handlerMethod": {
      "className": "com.myrefactor.monitoring.demoactuator.controller.IndexController",
      "name": "showMessage",
      "descriptor": "()Ljava/lang/String;"
    },
    "requestMappingConditions": {
      "consumes": [],
      "headers": [],
      "methods": [
        "GET"
      ],
      "params": [],
      "patterns": [
        "/say-hello-actuator"
      ],
      "produces": []
    }
  }
}
...
````
Awesome!. We could use actuator to provide documentation for the application endpoints.
> The tags "consumes", "headers", "produces", etc can be specified in @*Mapping annotations.

## Actuator configuration
For security purposes, you might choose to expose the actuator endpoints in different ports, for instance:
````commandline
#port used to expose actuator
management.port=8081 

#Address allowed to hit actuator
management.address=127.0.0.1

#Whether security should be enabled or disabled altogether
management.security.enabled=false
````

If the application is using Spring Security, we could secure these endpoints by defining username, password, etc. in the *application.properties* file:
````commandline
security.user.name=admin
security.user.password=secret
management.security.role=SUPERUSER
````
In subsequent entries, we will cover how to extend/modify the endpoint and also how to add custom endpoints to actuator.

## Conclusion
In this Spring Boot Actuator post, we have covered the fundamentals of the Actuator tool, we went through a few endpoints like metrics and mapping. 
We also discussed how different configuration options are available to secure the power of these endpoints.