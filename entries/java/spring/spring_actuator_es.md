## visi&oacute;n general
Este art&iacute;culo presentar&aacute; la herramienta Actuator para monitorear y administrar aplicaciones de Spring Framework. Aprender&aacute; a usar algunos puntos finales como m&eacute;tricas y configuraciones necesarias como Seguridad.

## Introducci&oacute;n
Spring Boot Actuator incluye una serie de caracter&iacute;sticas adicionales para ayudarlo a monitorear y administrar su aplicaci&oacute;n cuando se pone en producci&oacute;n. Puede elegir administrar y monitorear su aplicaci&oacute;n utilizando puntos finales HTTP, con JMX o incluso mediante un shell remoto (SSH o Telnet). La auditor&iacute;a, el estado y la recopilaci&oacute;n de m&eacute;tricas se pueden aplicar autom&aacute;ticamente a su aplicaci&oacute;n.

## Caracter&iacute;sticas de Actuator
* **Endpoints** Los endpoints de Actuator le permiten monitorear e interactuar con su
  aplicaci&oacute;n. Spring Boot incluye una serie de endpoints incorporados y tambi&eacute;n puede agregar
  tu propio.
* **Metrics** Spring Boot Actuator incluye un servicio de m&eacute;tricas con `gauge` y
  soporte `counter`. Un `gauge` registra un solo valor; y un `counter` registra un
  delta (un incremento o decremento). Las m&eacute;tricas para todas las solicitudes HTTP son autom&aacute;ticamente
  registradas, por lo que si alcanza el endpoint "metrics", deber&iacute;a ver una respuesta sensible.
* **Audit/Auditoria** Spring Boot Actuator tiene un marco de auditor&iacute;a flexible que publicar&aacute; eventos
  a un `AuditService`. Una vez que Spring Security est&aacute; en juego, publica autom&aacute;ticamente
  eventos de autenticaci&oacute;n por defecto. Esto puede ser muy &uacute;til para informar, y tambi&eacute;n para
  implementar una pol&iacute;tica de bloqueo basada en fallas de autenticaci&oacute;n.
* **Monitoreo de procesos** En Spring Boot Actuator puede encontrar `ApplicationPidFileWriter`
  que crea un archivo que contiene el PID de la aplicaci&oacute;n (por defecto en el directorio de la aplicaci&oacute;n
  con un nombre de archivo de `application.pid`).

## Dependencias
La forma m&aacute;s sencilla de activar Actuador en Spring Boot es agregar la dependencia del actuador al archivo *pom.xml*:
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

## Creando un controlador RESTFul sencillo
Vamos a crear un controlador Rest simple y exponer un punto final solo para ver c&oacute;mo Actuator toma la informaci&oacute;n relacionada con este punto final y c&oacute;mo podemos administrarlo.
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

## Comprobando si Actuador funciona
Ahora solo necesitamos ejecutar la aplicaci&oacute;n y dirigir nuestro navegador a la URL: [http://localhost:8080/actuator](http://localhost:8080/actuator). El navegador mostrar&aacute;:
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
Como puede ver, tenemos m&aacute;s rutas disponibles, as&iacute; que, por ejemplo, si va a: [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health), el resultado es:
````json
{"status":"UP"}
````
Esto significa que nuestra aplicaci&oacute;n est&aacute; "saludable" y en ejecuci&oacute;n.

### Cambiando el punto final predeterminado
Agregue la siguiente l&iacute;nea a "application.properties":
````commandline
management.endpoints.web.base-path=/manage
````
La propiedad anterior cambia la forma de las URL de */actuator/{id}* a */manage/{id}*.
Por ejemplo, la URL para consultar la salud se convertir&iacute;a en */manage/health*.

## Puntos finales de los actuadores
Actuator viene con muchos endpoint, habilit&eacute;moslos todos para ver qu&eacute; tan poderosa es esta herramienta, incluya lo siguiente en "application.properties":
````xml
management.endpoints.web.exposure.include=*
````
Vuelva a ejecutar la aplicaci&oacute;n y vaya de nuevo a [http://localhost:8080/actuator](http://localhost:8080/actuator), el resultado ahora es diferente:
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
Interesante ¿no?. Podr&iacute;amos excluir algunos puntos finales que quiz&aacute;s no desee utilizar, por ejemplo:
````commandline
management.endpoints.web.exposure.exclude=loggers
````
Esto excluir&aacute; todos los puntos finales relacionados con el *logging* o registro.

## Usando el punto final de m&eacute;tricas.
A los efectos de este tutorial, vamos a utilizar el endpoint de m&eacute;tricas.
Vaya a: [http://localhost:8080/actuator/metrics](http://localhost:8080/actuator/metrics), puede ver todas las m&eacute;tricas del actuador a continuaci&oacute;n:
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
Ahora vamos a crear un punto final para obtener el uso de la CPU, combinando el endpoint:
`http://localhost:8080/actuator/metrics/{requiredMetricName}` con el nombre de la m&eacute;trica `jvm.threads.live`. 
As&iacute; que abra el navegador en: [http://localhost:8080/actuator/metrics/jvm.threads.live](http://localhost:8080/actuator/metrics/jvm.threads.live), y el resultado es
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
Lo que significa que mi JVM tiene 22 subprocesos activos en este momento.

## Comprobaci&oacute;n de las URLs o "mappings"
¿Recuerdas nuestro controlador verdad?, no hemos visto ninguna estad&iacute;stica relacionada con &eacute;l. Verifiquemos el endpoint de mapeo expuesto por Actuator. Vaya a [http://localhost:8080/actuator/mappings](http://localhost:8080/actuator/mappings), habr&aacute; mucha informaci&oacute;n, pero nuestra url definida en el controlador estar&aacute; all&iacute;:
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
¡Impresionante!. Podr&iacute;amos usar Actuador para proporcionar documentaci&oacute;n para los endpoints de la aplicaci&oacute;n.
> Las etiquetas "consume", "headers", "produce", etc. se pueden especificar en las anotaciones @*Mapping.

## Configuraci&oacute;n de Actuador
Por motivos de seguridad, puede optar por exponer los endpoint de Actuador en diferentes puertos, por ejemplo:
````commandline
#port used to expose actuator
management.port=8081 

#Address allowed to hit actuator
management.address=127.0.0.1

#Whether security should be enabled or disabled altogether
management.security.enabled=false
````

Si la aplicaci&oacute;n utiliza Spring Security, podr&iacute;amos proteger estos endpoints definiendo el nombre de usuario, la contrase&ntilde;a, etc. en el archivo *application.properties*:
````commandline
security.user.name=admin
security.user.password=secret
management.security.role=SUPERUSER
````
En entradas posteriores, abarcaremos c&oacute;mo extender/modificar endpoints y tambi&eacute;n c&oacute;mo agregar endpoints personalizados a Actuador.

## Conclusi&oacute;n
En esta publicaci&oacute;n de Spring Boot Actuator, cubrimos los fundamentos de la herramienta Actuator, revisamos algunos puntos finales como m&eacute;tricas y mapeo.
Tambi&eacute;n discutimos c&oacute;mo las diferentes opciones de configuraci&oacute;n est&aacute;n disponibles para asegurar el poder de estos puntos finales.