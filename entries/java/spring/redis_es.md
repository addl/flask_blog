
## Requisitos
1. Docker Desktop instalado
2. Java JDK 1.8+
3. Un editor de texto o tu IDE favorito

## Instalar Redis usando Docker
Con Docker instalado, ejecute el siguiente comando en la l&iacute;nea de comandos:
````commandline
docker run --name my-redis -p 6379:6379 -d redis
````
El comando anterior realizar&aacute; lo siguiente:  

* Descargar la &uacute;ltima imagen de Redis del repositorio de Docker
* Crear un contenedor llamado "my-redis" y ejecutarlo
* Enlazar el puerto 6379 en mi computadora port&aacute;til al puerto 6379 dentro del contenedor. 6379 es el puerto predeterminado utilizado por Redis

Para confirmar que redis se est&aacute; ejecutando y escuchando en el puerto 6379, ejecute:
````commandline
docker ps
````
La salida debe ser:
````commandline
C:\Users\MyRefactor>docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                    NAMES
7a98d474f9b2   redis     "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes   0.0.0.0:6379->6379/tcp   my-redis
````
Ahora que hemos configurado Redis, escribamos nuestra aplicaci&oacute;n Spring para conectarse, almacenar y recibir informaci&oacute;n.

## dependencias de maven
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

## Creando el controlador y el DTO
Crearemos un controlador que recibir&aacute; la informaci&oacute;n que queremos almacenar en Redis. 
Para recibir datos en el controlador, estoy un Objeto de Transferencia de Datos (DTO) que representa a un usuario:
````java
public class User {

  private String username;
  private String url;

  public User() {

  }

  // getters and setters
}
````
Usaremos el atributo "username" como clave y la "url" como valor para almacenarlos en Redis. 
Ahora vamos a crear el controlador:
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
En el c&oacute;digo anterior, el controlador es **@RestController** para recibir y devolver datos mediante JSON. Vamos a repasarlo para entenderlo:  

* Spring Boot proporciona un RedisTemplate que estamos inyectando en nuestro controlador. Podr&iacute;amos usar una capa de servicio, pero por simplicidad la estamos usando directamente en el controlador.
* Hemos declarado un m&eacute;todo que recibe un objeto "User" en JSON usando el m&eacute;todo POST y **@RequestBody**.
* Estamos utilizando la operaci&oacute;n "opsForList()" y su m&eacute;todo "leftPush" para almacenar como clave el nombre de usuario y como valor la URL.
* Tambi&eacute;n declaramos un m&eacute;todo para obtener el valor de una clave pasada como par&aacute;metro usando **@RequestParam**.
* Finalmente, estamos usando nuevamente la operaci&oacute;n "opsForList()", pero esta vez el m&eacute;todo es "leftPop" para recuperar el valor de la clave de Redis y eliminarlo al mismo tiempo.

## Running and Testing
Para probar nuestro c&oacute;digo, primero debemos iniciar el servidor Spring:
````commandline
mvn spring-boot:run
````
Si el servidor se est&aacute; ejecutando, ver&aacute; en la consola una salida similar a esta:
````commandline
Tomcat started on port(s): 8080 (http) with context path ''
````
Ahora enviaremos una solicitud POST con el siguiente payload:
````json
{
    "username": "myrefactor",
    "url": "http://myrefactor.com/"
}
````
Puede usar CURL de la siguiente manera:
````json
curl --location --request POST 'http://127.0.0.1:8080/store' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "myrefactor",
    "url": "http://myrefactor.com/"
}'
````
O en mi caso, estoy usando Postman:

![Request to controller using Postman](https://drive.google.com/uc?id=1LfrWyPCuwzcSMEnCUlJbShDOH5wEnhSu)

Como puede ver, la respuesta es "OK", lo que significa que la clave: "myrefactor" y el valor: "http://myrefactor.com/" se almacenaron correctamente en Redis.
Para confirmarlo, solicitemos el valor mediante la solicitud GET, abra su navegador en la siguiente direcci&oacute;n:

[http://127.0.0.1:8080/retrieve?username=myrefactor](http://127.0.0.1:8080/retrieve?username=myrefactor)

Si recibe el texto:
````json
http://myrefactor.com/
````
Significa que ha recuperado el valor con &eacute;xito. ¡Felicidades!

> Despu&eacute;s de recuperar el valor, Redis eliminar&aacute; autom&aacute;ticamente la clave debido a que estamos usando el m&eacute;todo "leftPop", por lo que despu&eacute;s de unos segundos ya no podr&aacute; recibir el valor.

## Resumen
Hemos desarrollado desde cero una aplicaci&oacute;n sencilla utilizando Redis y Spring Boot. Hay mucho que cubrir con respecto a Redis y Spring Data. No obstante, espero que esta gu&iacute;a te haya servido para dar tus primeros pasos.