## Que es Hibernate

Hibernate es una herramienta de asignaci&oacute;n de objeto / relacional. Es muy popular entre las solicitudes de Java e implementa la API Persistence Java. Hibernate Orm permite a los desarrolladores escribir aplicaciones m&aacute;s f&aacute;cilmente cuyos datos sobreviven el proceso de solicitud. Como marco de objetos / mapeo relacional (ORM), Hibernate se refiere a la persistencia de datos, ya que se aplica a las bases de datos relacionales (a trav&eacute;s de JDBC)

## Maven dependencias

````xml
<dependencies>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

</dependencies>
````
He incluido **spring-boot-starter-web** para que Spring ejecute un servidor y podamos acceder a la base de datos en la memoria.

## Base de datos en memoria con H2

Las dependencias anteriores son suficientes para tener una base de datos en memoria, al ejecutar la aplicaci&oacute;n:

````commandline
mvn spring-boot:run
````

Podemos detectar en la salida de la consola las siguientes l&iacute;neas:

````commandline
2022-04-25 08:28:26.147  ...    : H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:49a11a51-3654-4811-b4c4-dc958006f12c'
2022-04-25 08:28:26.207  ...    : HHH000204: Processing PersistenceUnitInfo [name: default]
````

Lo que significa que podemos acceder a nuestra base de datos utilizando la URL:

````commandline
jdbc:h2:mem:49a11a51-3654-4811-b4c4-dc958006f12c
````

Abre el navegador en la direcci&oacute;n: [http://localhost:8080/h2-console](http://localhost:8080/h2-console), y coloque dentro de la caja de "JDBC URL" la URL de la base de datos, de la siguiente manera:

![New Project using PyCharm](https://drive.google.com/uc?id=13w3PF0BCd064d8-lelgS3pm_v0Fbe7JE)

Una vez que haga clic en el boton "Connect", debe ver la siguiente interfaz:

![New Project using PyCharm](https://drive.google.com/uc?id=1RJHfQUpD3FpqWiLFSlJIGqN3D4Soq-JN)

> Cada vez que ejecuta la aplicaci&oacute;n, URL de la base de datos es diferente.

## Creando el modelo

Defina una clase "Book" simple que represente la tabla de nuestra base de datos:

````java
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Book {

    @Id
    @GeneratedValue
    private Long id;
    private String name;

    public Book() {
    }

    // getters ans setters
}
````

Con la clase de entidad anterior, Hibernate crear&aacute; la tabla de la base de datos para nosotros, ejecute la aplicaci&oacute;n nuevamente para confirmar, inicie sesi&oacute;n nuevamente en la base de datos:

![New Project using PyCharm](https://drive.google.com/uc?id=1_oCn_ZDcLpHv_4-_PJZOCzMmRLMFcxeT)

Observe c&oacute;mo se ha creado la tabla "BOOK" junto con las columnas "ID" y "NAME", haciendo clic en el nombre de la tabla, podemos ver una consulta simple para obtener todos los libros almacenados en la base de datos, haga clic en el bot&oacute;n de flecha verde para ejecutar la consulta, como puede ver, no hay resultados, pues la base de datos est&aacute; vac&iacute;a:
## Ejecutar SQL por defecto

Cuando Spring se ejecuta, si Hibernate encuentra un archivo "import.sql" en la carpeta de recursos, lo ejecutar&aacute; para nosotros. Podemos usar este archivo para rellenar la base de datos. As&iacute; que vamos a crear un archivo llamado "import.sql" con el siguiente contenido:

````sql
insert into book values(1, 'Pride and Prejudice');
insert into book values(2, 'The Iliad');
insert into book values(3, 'The Decameron');
````
El script de SQL anterior agrega tres libros a nuestra base de datos. Vuelva a ejecutar la consulta SQL para confirmar que nuestra base de datos est&aacute; poblada:

![New Project using PyCharm](https://drive.google.com/uc?id=1qyIe13vDG8VZHPQipLTI-3nnMpzfCTEj)

Ahora, cada vez que ejecutamos el sistema, Spring crea una base de datos en memoria y agrega tres libros, por lo que tenemos una configuraci&oacute;n de base de datos para jugar.

## Creando el repositorio y el servicio

Dentro de un paquete llamado "Repository", creemos una interfaz y extienda **JpaRepository**, he llamado al archivo "BookRepository.java":

````java
@Repository
public interface BookRepository extends JpaRepository<Book, Long> {
}
````

He usado la anotaci&oacute;n **@Repository** para indicarle a Spring que este es un componente que interact&uacute;a con la base de datos y debe cargarse en el contexto.
Aunque podemos utilizar directamente los repositorios en los controladores de Spring, siempre es una buena idea tener un servicio que utiliza el repositorio para acceder a la base de datos.
Personalmente, utilizo los servicios para implementar la l&oacute;gica de negocio, por ejemplo, el proceso para prestar un libro a un usuario en nuestro sistema. 
Pero por el bien de este tutorial, solo mostraremos todos los libros en la base de datos. Vamos a crear la capa de servicio. Dentro de un paquete llamado "service", cree una clase "BookService" con el siguiente contenido:
````java
import com.myrefactor.spring.hibernate.model.Book;
import com.myrefactor.spring.hibernate.repository.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookService {
    private BookRepository bookRepository;

    @Autowired
    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

}
````

He anotado la clase usando **@Service** para indicar que este es un componente, en el constructor, tambi&eacute;n he usado **@Autowired** para que Spring pueda satisfacer la dependencia "BookRepository".
Tambi&eacute;n tenemos el m&eacute;todo "getAllBooks()" para obtener todos los libros en la base de datos utilizando el repositorio de libro "BookRepository".

## Creando el controlador

Ahora crear&aacute; un simple **@RestController** para devolver todos los libros en formato JSON. Cree un paquete de "controllers" y dentro crea una clase "BookController.java" y agrega este contenido:

````java
import com.myrefactor.spring.hibernate.model.Book;
import com.myrefactor.spring.hibernate.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class BookController {

    @Autowired
    private BookService bookService;

    @GetMapping("/books")
    public List<Book> getBooks(){
        return bookService.getAllBooks();
    }
}
````

Al usar **@RestController** estamos creando un controlador para el cual el contenido siempre se formatear&aacute; en JSON. Adem&aacute;s, estoy inyectando el componente "BookService" utilizando **@Autowired** en la propiedad.
Finalmente, la anotaci&oacute;n **@GetMapping** indica la URL bajo la cual se puede acceder a todos los libros.

## Running the application

Vamos a ejecutar nuestro sistema:

````commandline
mvn spring-boot:run
````
Y abra su navegador en la URL: [http://127.0.0.1:8080/books](http://127.0.0.1:8080/books)

Deber&iacute;as ver todos los libros:

![New Project using PyCharm](https://drive.google.com/uc?id=1uaE-uj0bULGN0D_1-eqMivtoTdfV8aXO)

## Conclusion

En este tutorial, hemos cubierto los pasos m&aacute;s simples para crear una aplicaci&oacute;n Spring utilizando Hibernate. En art&iacute;culos subsiguientes, abordaremos caracter&iacute;sticas m&aacute;s avanzadas.