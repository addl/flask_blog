## What is Internationalization?
Una de las características clave de Spring es su compatibilidad con la internacionalización (I18n), que se refiere al proceso de adaptación del software para admitir múltiples idiomas y configuraciones regionales. Esto es cada vez más común en los sistemas modernos ya que pretenden llegar a más clientes.

## Introducción
En este artículo, abordaremos cómo lograr I18n en aplicaciones Spring. El proyecto consiste en configurar una API Rest que soporte i18n.

## Notas generales
En una aplicación Spring, I18n normalmente se implementa mediante la clase `ResourceBundleMessageSource`, que carga cadenas de mensajes de archivos de propiedades que se nombran de acuerdo con las convenciones de Java para paquetes de recursos de I18n. Por ejemplo, un paquete de mensajes para inglés podría almacenarse en un archivo llamado `messages_en.properties`, mientras que un paquete de mensajes para español podría almacenarse en un archivo llamado `messages_es.properties`.

Spring también brinda soporte para formatear mensajes con marcadores de posición, utilizando la clase `MessageFormat`. Esto le permite incluir valores dinámicos en sus mensajes, como nombres de usuario o fechas, sin tener que concatenar cadenas manualmente.

## Archivos de mensajes
Dentro de la carpeta `src/main/resources` cree un archivo `messages.properties` y dentro del texto:

````
greeting=Hello, {0}!
````

Esto significa que nuestra clave para este mensaje es `greeting` y el mensaje real será el texto Hola seguido de un marcador de posición que puede recibir cualquier valor, por ejemplo, un nombre.

De forma similar a la anterior, cree otro archivo dentro de la misma carpeta de nombre `messages_es.properties` con el texto:

````
greeting=Hola, {0}!
````

Observe cómo este archivo termina con `_es` especificando de esa manera que este archivo se usa para el idioma español.

> Cuando no se añade ningún sufijo al archivo de mensajes como en `messages.properties`, este archivo se utiliza para la configuración predeterminada.

## Dependencias
````xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
````

## El controlador
Vamos a crear un controlador Rest de la siguiente manera:

````java
@RestController
public class GreetingsController {

  @Autowired
  private MessageSource messageSource;

  @GetMapping("/greeting")
  public String greeting(
      @RequestParam(name = "name", required = false, defaultValue = "World") String name) {
    return messageSource.getMessage("greeting", new Object[] {name},
        LocaleContextHolder.getLocale());
  }

}
````

En el código anterior estamos inyectando un bean de tipo `MessageSource` que nos permite acceder a los mensajes almacenados en los archivos a través del método `getMessage`. También declaramos una API URL `/saludo` que recibe un parámetro `name` y devuelve el mensaje.

Es crucial darse cuenta de cómo obtenemos el lenguaje actual accediendo estáticamente a `LocaleContextHolder.getLocale()`. 

Spring puede seguir varias estrategias para definir el locale, proceso conocido también como `Locale Resolver`, los locale resolver pueden utilizar Sessions, Cookies, HTTP Headers, etc. Definiremos nuestra estrategia en la siguiente sección.

## Configuración de frijoles
Nuestra configuración es la más simple, declaramos un Locale resolver por encabezados HTTP, de la siguiente manera:

````java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {


  @Bean
  public LocaleResolver localeResolver() {
    AcceptHeaderLocaleResolver ahlr = new AcceptHeaderLocaleResolver();
    ahlr.setDefaultLocale(Locale.US);
    return ahlr;
  }

}
````

Arriba creamos un bean de tipo `LocaleResolver`, concretamente `AcceptHeaderLocaleResolver`, esta implementación simplemente usa el lenguaje especificado en el encabezado HTTP "accept-language".

> Este solucionador de configuración regional no es compatible con `setLocale`, ya que el cliente está a cargo de pasar el encabezado y Spring resolverá ese idioma.

## Probando la API
Eso es todo lo que necesita para configurar una API Rest compatible con i18n, realicemos algunas pruebas. Usando CURL por ejemplo:

````
curl --location --request GET "http://localhost:8080/greeting?name=MyRefactor"

Hello, MyRefactor!
````

Ahora usando el encabezado `Accept-Language`:

````
curl --location --request GET "http://localhost:8080/greeting?name=MyRefactor" --header "Accept-Language: es"

Hola, MyRefactor!
````

## Conclusiones
En este tutorial, aprendimos cómo admitir i18n fácilmente usando las propiedades del mensaje y el encabezado HTTP Accpet-Language, lo que le da la posibilidad al cliente de solicitar recursos en diferentes idiomas. esto también se puede aplicar a bases de datos o fuentes de datos externas especificando el idioma en el que queremos la información.

## References
[Guide to Internationalization in Spring Boot](https://www.baeldung.com/spring-boot-internationalization)