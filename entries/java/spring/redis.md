
## Requirements
1. Docker Desktop installed
2. Java JDK 1.8+
3. A text editor or IDE

## Installing Redis using docker
With Docker installed, execute the following command in the command line:
````commandline
docker run --name my-redis -p 6379:6379 -d redis
````
The above command will:

* Download the latest Redis image from the Docker repository
* Create container named "my-redis" and execute it
* Route port 6379 on my laptop to port 6379 inside the container. 6379 is the default port used by Redis

Confirming that redis is running and listening on port 6379, execute:
````commandline
docker ps
````
The output should be:
````commandline
C:\Users\MyRefactor>docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                    NAMES
7a98d474f9b2   redis     "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes   0.0.0.0:6379->6379/tcp   my-redis
````
Now that we have set Redis up, let's write our Spring application to connect, store and receive information.

## Maven dependencies
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
````

## Creating the controller and Dto
We will create a controller which receive the information we want to store in Redis. To receive data in the controller, I am creating a Data Transfer Object(DTO) class representing a User:
````java
public class User {

  private String username;
  private String url;

  public User() {

  }

  // getters and setters
}
````
We will use the attribute "username" as the key and the "url" as the value to store them in Redis. Now let's create the controller:
````java
import com.myrefactor.spring.redisexample.controllers.dto.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CacheController {

  @Autowired
  private RedisTemplate redisTemplate;

  @PostMapping("/store")
  public String storeUserLink(@RequestBody User user){
    redisTemplate.opsForList().leftPush(user.getUsername(), user.getUrl());
    return "OK";
  }

  @GetMapping("/retrieve")
  public Object getUserLink(@RequestParam("username") String username){
    return redisTemplate.opsForList().leftPop(username);
  }

}
````
In the above code, the controller is **@RestController** to receive and return data using JSON. Let's go through it to understand it:  

* Spring Boot provide a RedisTemplate that we are injecting in our controller. We could use a service layer, but for simplicity we are using it directly in the controller.
* We have declared a method which receive a "User" object in JSON using POST method and **@RequestBody**.
* We are using "opsForList()" operation and its method "leftPush" to store as key the username and as value the URL.
* We also declared a method to fetch the value of a given key passed as **@RequestParam**
* Finally, we are using again "opsForList()" operation, but this time the method is "leftPop" to retrieve the key's value from Redis and remove it at the same time.

## Running and Testing
In order to test our code, first we need to start the Spring server:
````commandline
mvn spring-boot:run
````
If the server is running, you will see in the console an output similar to this one:
````commandline
Tomcat started on port(s): 8080 (http) with context path ''
````
Now we will send a POST request with the following payload:
````json
{
    "username": "myrefactor",
    "url": "http://myrefactor.com/"
}
````
You can use CURL as following:
````json
curl --location --request POST 'http://127.0.0.1:8080/store' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "myrefactor",
    "url": "http://myrefactor.com/"
}'
````
Or in my case, I am using Postman:

![Request to controller using Postman](https://drive.google.com/uc?id=1LfrWyPCuwzcSMEnCUlJbShDOH5wEnhSu)

As you can see the response is "OK", which means that the key: "myrefactor" and the value: "http://myrefactor.com/" where successfully stored in Redis.  
To confirm it, let's request the value using the GET request, open your browser in the following address:  

[http://127.0.0.1:8080/retrieve?username=myrefactor](http://127.0.0.1:8080/retrieve?username=myrefactor)

If you receive the text: 
````json
http://myrefactor.com/
````
It means you have retrieved the value successfully. Congratulations!

> After retrieving the value, Redis will automatically remove the key due to we are using "leftPop" method, so after few seconds you won't be able to receive the value anymore.

## Summary
We have developed from scratch a simple applicaction using Redis and Spring Boot. There is alot to cover in regards Redis and Spring Data. Nonetheless, I hope this guide has helped you in your first steps.