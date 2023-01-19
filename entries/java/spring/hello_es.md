## Introducción
Spring es un marco de código abierto para crear aplicaciones Java. Proporciona un modelo integral de programación y configuración para aplicaciones empresariales modernas basadas en Java. Spring es conocido por su capacidad para simplificar el desarrollo de aplicaciones complejas de nivel empresarial y su enfoque en proporcionar un marco cohesivo para todos los aspectos del ciclo de vida de una aplicación.
En esta entrada de blog, aprenderá cómo comenzar a crear una API simple.

## Generar proyecto
Lo primero es generar un proyecto. Para hacerlo, vaya a: [https://start.spring.io/](https://start.spring.io/)

Aqu&iacute; podemos generar un projecto b&aacute;sico, como ver&aacute;s vamos a usar Maven y Java y para este tutorial y usaremos como grupo "com.myrefactor.spring":

![New Project using PyCharm](https://drive.google.com/uc?id=1RJirQozB3p6Dg1KtcnH9SsYR7K5zoKAv)

En el panel derecho de la p&aacute;gina podemos especificar las dependencias, Spring posee varios m&oacute;dulos como AOP, Spring Data, etc. Para este tutorial solo necesitamos el m&oacute;dulo Web, para a&ntilde;adirlo demos click en el bot&oacute;n "ADD DEPENDENCIES":

![New Project using PyCharm](https://drive.google.com/uc?id=1CVdGn6L7spxTJleJ3kx0C27QY3kD0LKA)

Luego, dentro del cuadro de b&uacute;squeda, ingrese Web y seleccione el cuadrado verde sugerido:

![New Project using PyCharm](https://drive.google.com/uc?id=1oyWnAMRckcU8TqMWVYiNjekU-Yx6DtLp)

Finalmente, para generar el proyecto, haga clic en el bot&oacute;n "GENERAR" en la parte inferior de la p&aacute;gina. Esto descargar&aacute; un archivo *zip* que contiene nuestro proyecto, as&iacute; que extraigamos la carpeta en una ubicaci&oacute;n conveniente en su disco duro:

## Import IntelliJ

El pr&oacute;ximo paso es abrir nuestro proyecto Java en nuestro IDE, estoy usando IntelliJ de JetBrains. Entonces, una vez que IntelliJ est&eacute; abierto, vaya a File -> Open men&uacute; y busque la carpeta que extrajo del archivo zip, y haga clic en Abrir, deber&iacute;a tener el siguiente aspecto:

![New Project using PyCharm](https://drive.google.com/uc?id=1DmVSyQD1CO-vgipWNlMJpCVEtte0Aaeq)

Como puede notar, tenemos un archivo llamado:
```commandline
MyprojectApplication.java
```
La clase usa la anotaci&oacute;n **SpringBootApplication**, que le dice a Spring que este es el archivo principal que se ejecutar&aacute; cuando queramos ejecutar nuestro proyecto.

## Creating the controller

Antes de crear una clase que represente a nuestro controlador, creemos un paquete **controllers**, porque lo m&aacute;s probable es que desee crear m&aacute;s de un controlador e idealmente deber&iacute;an colocarse en un paquete dedicado solo para controladores. Despu&eacute;s de crear el paquete, cree una clase dentro de este paquete con el nombre "HelloController", de la siguiente manera:

![New Project using PyCharm](https://drive.google.com/uc?id=1VLsiTn2aEbQwiuOIFQsON_jOqk1MHROm)

Ahora debemos anotar esta clase con **@RestController** para indicar a Spring que este controlador recibir&aacute; solicitudes desde el navegador:

```java
package com.myrefactor.spring.myproject.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

}
```

Pero ahora, ¿qu&eacute; URL debe procesar este controlador? para indicar las URL hay varias anotaciones como **@RequestMapping** para fines generales o **@GetMapping** y **@PostMapping** que indican expl&iacute;citamente el m&eacute;todo HTTP utilizado, usaremos **@GetMapping** solo para fines demostrativos:

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

Ahora ejecutemos nuestro proyecto y confirmemos que nuestro controlador funciona correctamente, haga clic derecho en el archivo "MyprojectApplication.java" y seleccione "Run 'MyprojectApplication'" de la siguiente manera:

![New Project using PyCharm](https://drive.google.com/uc?id=1TYC8nTizHdyVtxK45V0rV4x8MiyXXDbO)

En su consola deber&iacute;a aparecer un mensaje similar a este:

```commandline
2022-04-20 16:56:53.952  INFO 10188 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-04-20 16:56:53.964  INFO 10188 --- [           main] c.m.s.myproject.MyprojectApplication     : Started MyprojectApplication in 3.664 seconds (JVM running for 4.375)
```
Si ese es el caso, vayamos a nuestro navegador favorito y escribamos la URL: [http://127.0.0.1](http://127.0.0.1), y el resultado debe ser:

![New Project using PyCharm](https://drive.google.com/uc?id=18leaWgojc8rjeJlSPnTeRZNdLbbXh760)

Grandioso!