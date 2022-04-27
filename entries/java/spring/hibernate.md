## What's Hibernate

Hibernate is an Object/Relational Mapper tool. It's very popular among Java applications and implements the Java Persistence API. Hibernate ORM enables developers to more easily write applications whose data outlives the application process. As an Object/Relational Mapping (ORM) framework, Hibernate is concerned with data persistence as it applies to relational databases (via JDBC)

## Maven dependencies

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
I have included **spring-boot-starter-web** so that Spring runs a server, and we are going to use it to access/manage the database in memory, we will get to that point.

## H2 in memory database

The above dependencies are enough to have an in-memory database, by running the application:

````commandline
mvn spring-boot:run
````

We can spot in the console output the following lines:

````commandline
2022-04-25 08:28:26.147  ...    : H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:49a11a51-3654-4811-b4c4-dc958006f12c'
2022-04-25 08:28:26.207  ...    : HHH000204: Processing PersistenceUnitInfo [name: default]
````

Which means we can access our database by using the url:

````commandline
jdbc:h2:mem:49a11a51-3654-4811-b4c4-dc958006f12c
````

Open your browser in the URL: [http://localhost:8080/h2-console](http://localhost:8080/h2-console), and put inside the JDBC URL's box the database's URL, as follows: 

![New Project using PyCharm](https://drive.google.com/uc?id=13w3PF0BCd064d8-lelgS3pm_v0Fbe7JE)

Once you click connect, you should see the following interface:

![New Project using PyCharm](https://drive.google.com/uc?id=1RJHfQUpD3FpqWiLFSlJIGqN3D4Soq-JN)

> Every time you run execute the application we get different database's URL.

## Creating the model

Let's define a simple Book class which will represent our database's tables:
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

With the above entity class, Hibernate will create the database's table for us, re-run the application to confirm, and login again into the database:

![New Project using PyCharm](https://drive.google.com/uc?id=1_oCn_ZDcLpHv_4-_PJZOCzMmRLMFcxeT)

Notice how the table "BOOK" has been created along with the columns "ID" and "NAME", by clicking over the table's name we can see a simple query to get all the books stored in the database, click in the green arrow button to execute the query, as you can see there is no entries for book.

## Default SQL

When Spring runs, if Hibernate find a file "import.sql" in the resources' folder, it will execute it for us. We can use this file to populate the database. So let's create a file called "import.sql" with the following content:
````sql
insert into book values(1, 'Pride and Prejudice');
insert into book values(2, 'The Iliad');
insert into book values(3, 'The Decameron');
````
The above SQL script add three books to our database. Re-run the application to confirm that our database is populated:

![New Project using PyCharm](https://drive.google.com/uc?id=1qyIe13vDG8VZHPQipLTI-3nnMpzfCTEj)

Now, everytime Spring creates a in-memory database will populate it with three books, so we have a database setup to play with.

## Creating the repository and the service

Inside a package called "repository" let's create an interface and extend the **JpaRepository** from Spring Hibernate, I called "BookRepository.java":

````java
@Repository
public interface BookRepository extends JpaRepository<Book, Long> {
}
````

I have used the annotation **@Repository** to indicate Spring this is a component which interacts with datasource and should be loaded into the Spring's context. 
Although we can use directly the repositories in Spring controllers, it is always a good idea to have a service which uses the repository to access the database. 
I personally use the service to implement the business logic, for example, the process to lend a book to a user in our system. But for the sake of this tutorial, we will only show all the books in the database.
Let's create the service layer. Inside a package called "service", create a class "BookService" with the following content:

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

I have annotated the class using **@Service** to indicate this is a Spring component, in the constructor I have used also **@Autowired** so Spring can satisfy the "bookRepository" dependency.
We also have "getAllBooks()" method to get all books in the database.

## Creating the controller

Now I will create a simple **@RestController** to return all books in JSON format. Inside "controllers" package create a class "BookController.java" and append this content:

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

By using **@RestController** we are creating a controller for which content will always be parsed to JSON format. Also, I am injecting the "BookService" component by using **@Autowired**in the property. 
Finally, **@GetMapping** annotation indicate the URL under the which I am returning all books.

## Running the application

Let's run our app:
````commandline
mvn spring-boot:run
````
And open your browser in the URL: [http://127.0.0.1:8080/books](http://127.0.0.1:8080/books)

You should see all the books:

![New Project using PyCharm](https://drive.google.com/uc?id=1uaE-uj0bULGN0D_1-eqMivtoTdfV8aXO)

## Conclusion

In this tutorial we have covered the simplest steps to create a Spring Boot application using Hibernate ORM. In subsequent articles we will be covering more advanced features
