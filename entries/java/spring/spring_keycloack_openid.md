## cover
![Keycloak Realm Creation](https://drive.google.com/uc?id=1Yyx0vqsrPJW5YN_-ny7GvL_6mlGy0OSx)


## Introduction
As modern applications are shifting towards microservices, it is becoming more important to provide a secure and scalable way to authenticate users across multiple services. One of the ways to achieve this is by using OpenID Connect protocol. In this article, we will explore how to configure Keycloak with Spring Boot to enable OpenID Connect authentication.

## Keycloak
Keycloak is an open-source Identity and Access Management solution that provides Single Sign-On (SSO), OAuth2, and OpenID Connect protocols. It provides a lot of features such as authentication, authorization, and user management, which can be used to secure our applications.

Before we dive into the configuration, let's quickly understand the terms used in Keycloak. 

1. Realms: A realm is a container for a set of users, authentication methods, client applications, and groups. It represents a security boundary and provides a way to partition a Keycloak installation into independent units. 
2. Clients: A client represents an application that uses Keycloak for authentication and authorization. Clients can be web or mobile applications, and can be configured to use different authentication flows and protocols. 
3. Users: A user represents an entity that can be authenticated and authorized to access client applications. Users can be stored locally in Keycloak or can be imported from external identity providers. 
4. Authentication: Keycloak provides various authentication mechanisms, including username and password, social identity providers (such as Google and Facebook), and multi-factor authentication. 

## Setting up Keycloak

### The realm
To get started, let's create a new realm in Keycloak by following these steps:

1. Open Keycloak administration console and log in as admin. 
2. Click on "Add realm" and enter a name for the new realm. 
3. Click "Create" to create the realm. 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1Ts2lIYIPymMZx7FMwDd5nb1uzKT_cRWV)

### The client
Now that we have created a new realm, let's create a client for this realm. A client is an application or service that is protected by Keycloak. Here are the steps to create a new client:

1. Navigate to the newly created realm and click on "Clients" on the left panel. 
2. Click on "Create" on the right side of the screen. 
3. Enter a name for the client and select "openid-connect" as the client protocol. 
4. Click on "Save". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1qc51uma2uPe7vnVvgnABOq138Ag8HwDR)

### The user
Now that we have created a new realm, and a client. We need to add users:

1. Navigate to the menu "Users" on the left panel. 
2. Click on "Add user" on the right side of the screen. 
3. Enter a name for the client, in my case "myrefactor-client". Used later on Spring configuration! 
4. Enter all details as shown in the picture below. 
5. Click on "Save". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1W-xEwVA8FZOGBx0lIyenPCy0B9F03oCN)

We need now to set up credentials for the newly created user, to do that: 

1. Navigate to the menu "Users" on the left panel. 
2. Click in "View all users". 
3. Click in the only user in the list. 
4. Navigate to the tab "Credentials". 
5. Fill out "Password" and "Password Confirmation" fields. 
6. Click on "Set Password". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1xiNk4l6HeVL3ccTQ9b2md8PIFknkxGVg)

Finally, since we set up the credentials manually, Keycloak will require actions for the users as follows: 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1eF3Xv0T5qxEx5wa9QDEbdcnfmkmnVgLN)

We have to ensure that the list of "Required User Actions" is empty. To do that, remove "Update Password" and click "Save"

> In Keycloak, a client represents an application or service that wants to authenticate its users and access resources on behalf of those users. On the other hand, a user is an entity that can authenticate to the system

## Spring project
Now that we have configured Keycloak, let's see how we can integrate it with Spring Boot. We will be using the Spring Security framework and the adapter for Keycloak to secure our REST endpoints.

### Dependencies
Add the following dependencies to your pom.xml file:
````xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.keycloak</groupId>
        <artifactId>keycloak-spring-boot-starter</artifactId>
        <version>17.0.0</version>
    </dependency>
</dependencies>
````

### Project properties
Add the following configuration to your application.properties file: 

````commandline
server.port: 9000

keycloak.realm=myrefactor
keycloak.auth-server-url=http://127.0.0.1:8080/auth/
keycloak.resource=myrefactor-client
keycloak.bearer-only: true
````

* The first property `server.port` sets the port number on which the Spring Boot app will be running. 
* The `keycloak.realm` property specifies the name of the realm that the Spring Boot app is associated with. 
* The `keycloak.auth-server-url` property specifies the URL of the Keycloak server. 
* The `keycloak.resource` value has tobe the name of the client we set up in keycloak. 
* Lastly `keycloak.bearer-only` is a boolean flag that specifies that Spring Boot app will only accept requests with a valid bearer token. 

### Security settings
Create a new class named `WebSecurityConfiguration` that extends `KeycloakWebSecurityConfigurerAdapter` and add the following content:

````java
@Configuration
public class WebSecurityConfiguration extends KeycloakWebSecurityConfigurerAdapter {

  @Autowired
  public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
    KeycloakAuthenticationProvider keycloakAuthenticationProvider =
        keycloakAuthenticationProvider();
    keycloakAuthenticationProvider.setGrantedAuthoritiesMapper(new SimpleAuthorityMapper());
    auth.authenticationProvider(keycloakAuthenticationProvider);
  }

  @Bean
  @Override
  protected SessionAuthenticationStrategy sessionAuthenticationStrategy() {
    return new NullAuthenticatedSessionStrategy();
  }

  @Override
  protected void configure(HttpSecurity http) throws Exception {
    super.configure(http);
    http.csrf().disable().authorizeRequests().antMatchers(HttpMethod.GET, "/users/**")
        .authenticated().anyRequest().permitAll();
  }

}
````
In this Spring Security configuration class, the **configureGlobal()** method sets up Keycloak as the authentication provider and the **configure()** method configures the HTTP security of the application, allowing authenticated users to access the `/users` endpoint using the GET method. 

> The **sessionAuthenticationStrategy()** method returns a NullAuthenticatedSessionStrategy to disable the default session authentication strategy.

### Spring controller
For the purpose of this tutorial create this simple controller:
````java
@RestController
@RequestMapping("/users")
public class UserController {

  @GetMapping("/all")
  public List<String> hello() {
    return Arrays.asList("admin", "recruiter");
  }

}
````
This controller class for a RESTful web service that listens to GET requests on the `/users/all` endpoint, and returns a list of strings containing representing virtual users.

## Testing the integration
Now we are ready to run the application, once is running let's make a call to our endpoint by using curl:
````commandline
curl --request GET "http://localhost:9000/users/all"
````
As you can see the response is:
````json
{
   "timestamp":"2023-03-07T14:16:01.514+0000",
   "status":401,
   "error":"Unauthorized",
   "message":"Unauthorized",
   "path":"/users/all"
}
````
This means we are not Authorized to access to the resource `/users/all` because Spring is expecting a valid token from Keycloak. So our first step should be to get the token

In order to get the token we have to send an HTTP request to Keycloak using the corresponding parameters, for example using curl:

````commandline
curl --location --request POST "http://127.0.0.1:8080/auth/realms/myrefactor/protocol/openid-connect/token" --header "Content-Type: application/x-www-form-urlencoded" --data-urlencode "client_id=myrefactor-client" --data-urlencode "username=myrefactor" --data-urlencode "password=test" --data-urlencode "grant_type=password"
````

Or if you prefer Postman, the request should look like this:

![Keycloak Realm Creation](https://drive.google.com/uc?id=1IY_5LOT8AM7LEVhVO28e5cGxJthPSBE5)

In any case the response from Keycloak should be similar as follows:
````json
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlajlqUEFDbGpRekxuUmhGMDBGMnk5eWkxNklIUkJ3UXYyQXZKN2ZNbFowIn0.eyJleHAiOjE2NzgxOTkyOTMsImlhdCI6MTY3ODE5ODk5MywianRpIjoiODg0NzM1NDAtMjhhMy00NDQyLWIwZDktOWExNTkyMzI1YzY4IiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDgwL2F1dGgvcmVhbG1zL215cmVmYWN0b3IiLCJzdWIiOiJjOWQ3ZDA0Ny01NTU4LTRhMWUtYmUyOS0yYjllMjk0MjdlNDkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJteXJlZmFjdG9yLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI3MWM2MmUwYS1hMzM1LTQyZjQtOGEzYi05MTVlOTlkYTVlZWYiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm1yYWRtaW4iXX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6IjcxYzYyZTBhLWEzMzUtNDJmNC04YTNiLTkxNWU5OWRhNWVlZiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiTVkgUmVmYWN0b3IgQ2xlYW4gY29kZSIsInByZWZlcnJlZF91c2VybmFtZSI6Im15cmVmYWN0b3IiLCJnaXZlbl9uYW1lIjoiTVkgUmVmYWN0b3IiLCJmYW1pbHlfbmFtZSI6IkNsZWFuIGNvZGUiLCJlbWFpbCI6ImFkbWluQG15cmVmYWN0b3IuY29tIn0.Wlln2FH-eUHaQgjvuby9YbjuazGPQ9Yh9nLYXPAumyYMik4w_v4yD2s6ywTdkyAszPYsVhgnfNmRQnTe1ueGPTHw9l5Ru7tHXrPnlUTnRepd40mnY6UdWhvFtMcW9RZoeGt13d13gCpuII8C5EtQld2mqXECQRZWIQ1ld5Gc1iN-GJoFPTkdo1V6TqKNfjhBh2599w_yMa7w69cwqKvUPqz0o8YZU3MetpF0Wb2bSFEAD80NB7AO4593Gs29HND82vroBvkL9j02vNQTaJoqOeWn6vgB4ZBg7j-mFAegYDO1F5-uzQ5UOdASdgM9w1zgzs1Ts48EbrBHQTJ3ihospw",
    "expires_in": 299,
    "refresh_expires_in": 1800,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI2MjI5MjRmMy1jM2E1LTQ0ZWQtOGM0MS04NmU4YmNhNWZiNGUifQ.eyJleHAiOjE2NzgyMDA3OTQsImlhdCI6MTY3ODE5ODk5NCwianRpIjoiOTM0YTMwNzQtOTgzYS00MTE0LWJmYWQtNWY2YzdlMGQyMWEyIiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDgwL2F1dGgvcmVhbG1zL215cmVmYWN0b3IiLCJhdWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwODAvYXV0aC9yZWFsbXMvbXlyZWZhY3RvciIsInN1YiI6ImM5ZDdkMDQ3LTU1NTgtNGExZS1iZTI5LTJiOWUyOTQyN2U0OSIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJteXJlZmFjdG9yLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI3MWM2MmUwYS1hMzM1LTQyZjQtOGEzYi05MTVlOTlkYTVlZWYiLCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI3MWM2MmUwYS1hMzM1LTQyZjQtOGEzYi05MTVlOTlkYTVlZWYifQ.QemHd8lEdq-NEsR0LYTiisEx5H6n-WbXkfHO2pTyen4",
    "token_type": "Bearer",
    "not-before-policy": 0,
    "session_state": "71c62e0a-a335-42f4-8a3b-915e99da5eef",
    "scope": "profile email"
}
````
Now we are going to use the `access_token` to make a request to Spring App, using curl again:

````commandline
curl --location --request GET "http://localhost:9000/users/all" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlajlqUEFDbGpRekxuUmhGMDBGMnk5eWkxNklIUkJ3UXYyQXZKN2ZNbFowIn0.eyJleHAiOjE2NzgxOTk4ODIsImlhdCI6MTY3ODE5OTU4MiwianRpIjoiMmM5YTg0OGItMTUwOC00YmYwLTliMmItYTU3MjczNzFlZTdmIiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDgwL2F1dGgvcmVhbG1zL215cmVmYWN0b3IiLCJzdWIiOiJjOWQ3ZDA0Ny01NTU4LTRhMWUtYmUyOS0yYjllMjk0MjdlNDkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJteXJlZmFjdG9yLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI3NzFmNWYzNy01MjBmLTRkYTItYTZmMi0zM2Q1MGMyYjQ3NjgiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm1yYWRtaW4iXX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6Ijc3MWY1ZjM3LTUyMGYtNGRhMi1hNmYyLTMzZDUwYzJiNDc2OCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiTVkgUmVmYWN0b3IgQ2xlYW4gY29kZSIsInByZWZlcnJlZF91c2VybmFtZSI6Im15cmVmYWN0b3IiLCJnaXZlbl9uYW1lIjoiTVkgUmVmYWN0b3IiLCJmYW1pbHlfbmFtZSI6IkNsZWFuIGNvZGUiLCJlbWFpbCI6ImFkbWluQG15cmVmYWN0b3IuY29tIn0.Vk7yjgwRKgO6YMU-0SFeYUd4ymBe6qJdX4CXGJtBTb8Kb9HxhYu1DKmJ1xNgaMkwwhgcm0VSEOwNcQyymQqwvw7dGshIl3KBVZ8JBaF6HOrbONKIXg-PVZUI-regiROK7OGmmfnjhzLYJ4JTR-E5Inh_cC43cvV1szDFlOsHVaeRBDA36D9GyqgLovY3ShmixoG4zlXfM38CwzZYYURy2n3oIiE3XttFftEe-vODyc3KjXcS0Sg1UXp4CCNJiTN0p_tmrL0VMgpOh5vdHU7rejm8dxo5nfxKhtmiWjYAAZ-R-S9M8dllWXwjqL8TVksGSPuSN516umH80-Ibdsoq9A"
````

Now the response from Spring is different:
````json
["admin", "recruiter"]
````

Congrats! We just integrated Keycloak and Spring using OpenID connect protocol.

## Conclusion
In this article, we have learned how to configure Keycloak with Spring Boot to enable OpenID Connect authentication. We crated a Spring application and secure our endpoint to use a valid Bearer token issued by Keycloak.
