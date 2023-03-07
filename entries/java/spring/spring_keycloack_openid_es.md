## cover
![Keycloak Realm Creation](https://drive.google.com/uc?id=1Yyx0vqsrPJW5YN_-ny7GvL_6mlGy0OSx)

## Introducción
A medida que las aplicaciones modernas se desplazan hacia los microservicios, se vuelve más importante proporcionar una forma segura y escalable de autenticar a los usuarios en múltiples servicios. Una de las formas de lograr esto es usando el protocolo OpenID Connect. En este artículo, exploraremos cómo configurar Keycloak con Spring Boot para habilitar la autenticación OpenID Connect.

## Capa de llaves
Keycloak es una solución de gestión de acceso e identidad de código abierto que proporciona protocolos de inicio de sesión único (SSO), OAuth2 y OpenID Connect. Proporciona muchas funciones, como autenticación, autorización y gestión de usuarios, que se pueden utilizar para proteger nuestras aplicaciones.

Antes de sumergirnos en la configuración, comprendamos rápidamente los términos utilizados en Keycloak.

1. Realms: un realm es un contenedor para un conjunto de usuarios, métodos de autenticación, aplicaciones cliente y grupos. Representa un límite de seguridad y proporciona una forma de dividir una instalación de Keycloak en unidades independientes. 
2. Clientes: un cliente representa una aplicación que utiliza Keycloak para autenticación y autorización. Los clientes pueden ser aplicaciones web o móviles y se pueden configurar para usar diferentes flujos y protocolos de autenticación. 
3. Usuarios: un usuario representa una entidad que se puede autenticar y autorizar para acceder a las aplicaciones del cliente. Los usuarios pueden almacenarse localmente en Keycloak o pueden importarse desde proveedores de identidad externos. 
4. Autenticación: Keycloak proporciona varios mecanismos de autenticación, incluidos nombre de usuario y contraseña, proveedores de identidad social (como Google y Facebook) y autenticación de múltiples factores. 

## Configuración de Keycloak

### El realm
Para comenzar, creemos un nuevo realm en Keycloak siguiendo estos pasos:

1. Abra la consola de administración de Keycloak e inicie sesión como administrador. 
2. Haga clic en "Add realm" e ingrese un nombre para el nuevo realm. 
3. Haga clic en "Create" para crear el realm. 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1Ts2lIYIPymMZx7FMwDd5nb1uzKT_cRWV)

### El cliente
Ahora que hemos creado un nuevo realm, creemos un cliente para este realm. Un cliente es una aplicación o servicio que está protegido por Keycloak. Estos son los pasos para crear un nuevo cliente:

1. Navegue hasta el realm recién creado y haga clic en "Clients" en el panel izquierdo. 
2. Haga clic en "Create" en el lado derecho de la pantalla. 
3. Introduzca un nombre para el cliente y seleccione "openid-connect" como protocolo de cliente. 
4. Haga clic en "Guardar". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1qc51uma2uPe7vnVvgnABOq138Ag8HwDR)

### El usuario
Ahora que hemos creado un nuevo realm y un cliente. Necesitamos agregar usuarios:

1. Navegue hasta el menú "Users" en el panel izquierdo. 
2. Haga clic en "Add user" en el lado derecho de la pantalla. 
3. Introduzca un nombre para el cliente, en mi caso "myrefactor-client". ¡Usado más tarde en la configuración de Spring! 
4. Ingrese todos los detalles como se muestra en la imagen a continuación. 
5. Haga clic en "Guardar". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1W-xEwVA8FZOGBx0lIyenPCy0B9F03oCN)

Ahora necesitamos configurar las credenciales para el usuario recién creado, para hacer eso:

1. Navegue hasta el menú "Users" en el panel izquierdo. 
2. Haga clic en "See all users". 
3. Haga clic en el único usuario de la lista. 
4. Navegue a la pestaña "Credentials". 
5. Complete los campos "Password" y "Password Confirmation". 
6. Haga clic en "Set Password". 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1xiNk4l6HeVL3ccTQ9b2md8PIFknkxGVg)

Finalmente, dado que configuramos las credenciales manualmente, Keycloak requerirá acciones para los usuarios de la siguiente manera: 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1eF3Xv0T5qxEx5wa9QDEbdcnfmkmnVgLN)

Tenemos que asegurarnos de que la lista de "Required User Actions" esté vacía. Para hacer eso, elimine "Update Password" y haga clic en "Save"

> En Keycloak, un cliente representa una aplicación o servicio que desea autenticar a sus usuarios y acceder a los recursos en nombre de esos usuarios. Por otro lado, un usuario es una entidad que puede autenticarse en el sistema.

## Proyecto de primavera
Ahora que hemos configurado Keycloak, veamos cómo podemos integrarlo con Spring Boot. Usaremos el marco Spring Security y el adaptador para Keycloak para asegurar nuestros puntos finales REST.

### Dependencias
Agregue las siguientes dependencias a su archivo `pom.xml`: 

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

### Propiedades del proyecto
Agregue la siguiente configuración a su archivo `application.properties`:

````commandline
servidor.puerto: 9000

keycloak.realm=mirefactor
keycloak.auth-server-url=http://127.0.0.1:8080/auth/
keycloak.resource=mirefactor-cliente
keycloak.bearer-only: verdadero
````

* La primera propiedad `server.port` establece el número de puerto en el que se ejecutará la aplicación Spring Boot. 
* La propiedad `keycloak.realm` especifica el nombre del dominio al que está asociada la aplicación Spring Boot. 
* La propiedad `keycloak.auth-server-url` especifica la URL del servidor Keycloak. 
* El valor de `keycloak.resource` tiene que ser el nombre del cliente que configuramos en keycloak. 
* Por último, `keycloak.bearer-only` es un indicador booleano que especifica que la aplicación Spring Boot solo aceptará solicitudes con un token de portador válido. 

### Configuraciones de seguridad
Cree una nueva clase llamada `WebSecurityConfiguration` que amplíe `KeycloakWebSecurityConfigurerAdapter` y agregue el siguiente contenido:

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

En esta clase de configuración de Spring Security, el método **configureGlobal()** configura Keycloak como proveedor de autenticación y el método **configure()** configura la seguridad HTTP de la aplicación, lo que permite a los usuarios autenticados acceder a `/users ` punto final utilizando el método GET.

> El método **sessionAuthenticationStrategy()** devuelve una NullAuthenticatedSessionStrategy para deshabilitar la estrategia de autenticación de sesión predeterminada.

### Controlador de resorte
Para el propósito de este tutorial, cree este controlador simple: 

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

Esta clase de controlador para un servicio web RESTful que escucha las solicitudes GET en el extremo `/users/all` y devuelve una lista de cadenas que contienen la representación de usuarios virtuales.

## Probando la integración
Ahora estamos listos para ejecutar la aplicación, una vez que se esté ejecutando, hagamos una llamada a nuestro punto final usando curl:

````commandline
curl --request GET "http://localhost:9000/users/all"
````

Como puedes ver la respuesta es: 

````json
{
   "timestamp":"2023-03-07T14:16:01.514+0000",
   "status":401,
   "error":"Unauthorized",
   "message":"Unauthorized",
   "path":"/users/all"
}
````

Esto significa que no estamos autorizados a acceder al recurso `/users/all` porque Spring espera un token válido de Keycloak. Así que nuestro primer paso debería ser obtener el token.

Para obtener el token, debemos enviar una solicitud HTTP a Keycloak usando los parámetros correspondientes, por ejemplo usando curl:

````commandline
curl --location --request POST "http://127.0.0.1:8080/auth/realms/myrefactor/protocol/openid-connect/token" --header "Content-Type: application/x-www-form-urlencoded" --data-urlencode "client_id=myrefactor-client" --data-urlencode "username=myrefactor" --data-urlencode "password=test" --data-urlencode "grant_type=password"
````

O si prefiere Postman, la solicitud debería verse así: 

![Keycloak Realm Creation](https://drive.google.com/uc?id=1IY_5LOT8AM7LEVhVO28e5cGxJthPSBE5)

En cualquier caso, la respuesta de Keycloak debería ser similar a la siguiente: 

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
Ahora vamos a usar el valor de `access_token` para hacer una solicitud a la aplicación Spring, usando curl nuevamente: 

````commandline
curl --location --request GET "http://localhost:9000/users/all" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlajlqUEFDbGpRekxuUmhGMDBGMnk5eWkxNklIUkJ3UXYyQXZKN2ZNbFowIn0.eyJleHAiOjE2NzgxOTk4ODIsImlhdCI6MTY3ODE5OTU4MiwianRpIjoiMmM5YTg0OGItMTUwOC00YmYwLTliMmItYTU3MjczNzFlZTdmIiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDgwL2F1dGgvcmVhbG1zL215cmVmYWN0b3IiLCJzdWIiOiJjOWQ3ZDA0Ny01NTU4LTRhMWUtYmUyOS0yYjllMjk0MjdlNDkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJteXJlZmFjdG9yLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI3NzFmNWYzNy01MjBmLTRkYTItYTZmMi0zM2Q1MGMyYjQ3NjgiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm1yYWRtaW4iXX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6Ijc3MWY1ZjM3LTUyMGYtNGRhMi1hNmYyLTMzZDUwYzJiNDc2OCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiTVkgUmVmYWN0b3IgQ2xlYW4gY29kZSIsInByZWZlcnJlZF91c2VybmFtZSI6Im15cmVmYWN0b3IiLCJnaXZlbl9uYW1lIjoiTVkgUmVmYWN0b3IiLCJmYW1pbHlfbmFtZSI6IkNsZWFuIGNvZGUiLCJlbWFpbCI6ImFkbWluQG15cmVmYWN0b3IuY29tIn0.Vk7yjgwRKgO6YMU-0SFeYUd4ymBe6qJdX4CXGJtBTb8Kb9HxhYu1DKmJ1xNgaMkwwhgcm0VSEOwNcQyymQqwvw7dGshIl3KBVZ8JBaF6HOrbONKIXg-PVZUI-regiROK7OGmmfnjhzLYJ4JTR-E5Inh_cC43cvV1szDFlOsHVaeRBDA36D9GyqgLovY3ShmixoG4zlXfM38CwzZYYURy2n3oIiE3XttFftEe-vODyc3KjXcS0Sg1UXp4CCNJiTN0p_tmrL0VMgpOh5vdHU7rejm8dxo5nfxKhtmiWjYAAZ-R-S9M8dllWXwjqL8TVksGSPuSN516umH80-Ibdsoq9A"
````

Ahora la respuesta de Spring es diferente: 

````json
["admin", "recruiter"]
````

¡Felicitaciones! Acabamos de integrar Keycloak y Spring usando el protocolo de conexión OpenID.

## Conclusión
En este artículo, hemos aprendido cómo configurar Keycloak con Spring Boot para habilitar la autenticación de OpenID Connect. Creamos una aplicación Spring y aseguramos nuestro punto final para usar un token de portador válido emitido por Keycloak.