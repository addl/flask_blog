## Qu&eacute; es Thymeleaf

Thymeleaf es un moderno motor de plantilla de Java Side Side para ambientes web y independientes.
El objetivo principal de Thymeleaf es traer plantillas naturales elegantes a su flujo de trabajo de desarrollo: HTML que se pueda mostrar correctamente en los navegadores y tambi&eacute;n trabajar como prototipos est&aacute;ticos, lo que permite una mayor colaboraci&oacute;n en los equipos de desarrollo.

## Objetivo

En este tutorial cubrir&eacute; los pasos m&aacute;s simples para crear un ejemplo de aplicaci&oacute;n Web con Spring Boot y Thymeleaf.

## Requisitos

1. JDK 8+ o OpenJDK 8+ 
2. Maven 3+ instalado
3. Tu IDE favorito

## Dependencias

Solo necesitamos dos dependencias para nuestro ejemplo: Web y Thymeleaf, por lo que en **pom.xml** configure las siguientes dependencias:

````commandline
...
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
...
````

## Creando el archivo HTML

Thymeleaf es HTML, por lo que vamos a crear un archivo HTML llamado: **index.html** dentro de la carpeta "templates":

![New Project using PyCharm](https://drive.google.com/uc?id=1jxevIMCmWgsIOlzafY-bqiR2UvhsSWd9)

Y dentro del archivo "index.html" ponemos el siguiente texto:

````html
<!DOCTYPE html>
<html>
   <head>
      <meta charset = "ISO-8859-1" />
      <link href = "css/styles.css" rel = "stylesheet"/>
      <title>Spring Boot Application</title>
   </head>
   <body>
      <h4>Welcome to Thymeleaf Spring Boot web application</h4>
   </body>
</html>
````

## Creando el controlador

Hasta ahora, hemos creado nuestra p&aacute;gina, pero tiene que ser servida por un controlador de Spring, una clase anotada con **@Controller**, vamos a crear uno.
Primero, creamos un paquete llamado "controladores":

![New Project using PyCharm](https://drive.google.com/uc?id=1Wwl9wVnkXCsf7hJW9qBpGHKJBtYkEORV)

Dentro de este paquete creamos una clase con nombre "IndexController.java", y dentro el siguiente contenido:

````java
package com.myrefactor.thymeleaf.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class IndexController {

    @RequestMapping(value = "/")
    public String index() {
        return "index";
    }

}
````

Es importante notar aqu&iacute; el uso de la anotaci&oacute;n **@Requestmapping**, b&aacute;sicamente le estamos diciendo a Spring que asigne el m&eacute;todo **index()** a la url "/" que es la ra&iacute;z de nuestro servidor.
Otro detalle es que devolvemos una cadena, que de manera predeterminada debe ser el nombre de la plantilla o el archivo HTML que queremos mostrar, en este m&eacute;todo devolvemos "index", por lo que Spring devolver&aacute; el archivo "index.html" ubicado dentro de la carpeta "templates".

## Ejecutando el proyecto

En la terminal, dentro de la carpeta del proyecto, ejecutamos:
````commandline
mvn spring-boot:run
````

Si todo sali&oacute; bien, deber&iacute;a ver algo similar a esta salida:

````commandline
2022-04-23 18:46:44.311  ... Tomcat started on port(s): 8080 (http) with context path ''
2022-04-23 18:46:44.316  ... Started ThymeleafApplication in 0.876 seconds (JVM running for 1.076)
````

Lo que significa que el servidor est&aacute; escuchando en el puerto 8080, por lo que vamos a abrir el navegador en la siguiente direcci&oacute;n:
[http://127.0.0.1:8080](http://127.0.0.1:8080)

En pantalla el resultado es el siguiente:

![New Project using PyCharm](https://drive.google.com/uc?id=18g3m3_dbWkGLBeZ51iV7H5ZZpAssnOsp)

Si&eacute;ntase libre de editar el HTML a su conveniencia, en otra publicaci&oacute;n discutiremos m&aacute;s caracter&iacute;sticas de Thymeleaf.