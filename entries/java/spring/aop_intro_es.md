## Introducci&oacute;n
En este tutorial, aprender&aacute; los conceptos fundamentales de la Programaci&oacute;n Orientada a Aspectos (tambi&eacute;n conocida como AOP) y crear&aacute; una aplicaci&oacute;n simple usando CommandLineRunner y Spring Boot.

## Terminolog&iacute;a de Programaci&oacute;n Orientada a Aspectos (AOP)

Podr&iacute;a decirse que AOP es un paradigma de programaci&oacute;n que aumenta la modularidad al separar las preocupaciones transversales dentro de una aplicaci&oacute;n.
Logra esto agregando un comportamiento adicional al c&oacute;digo existente sin modificarlo.
Muchas fuentes se refieren a &eacute;l como un complemento de la Programaci&oacute;n Orientada a Objetos en lugar de un paradigma.
En pocas palabras, la siguiente imagen deber&iacute;a proporcionarle una comprensi&oacute;n general de AOP.  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1UmEZOzg_0MwwyeFTq2dWiBP7bi5V1w3X)

### Aspecto
En la imagen de arriba, las l&iacute;neas horizontales representan capas de una aplicaci&oacute;n, mientras que las l&iacute;neas verticales representan aquellas operaciones que son "verticales" para casi cualquier funcionalidad, como **logging** y **seguridad**.
Estas operaciones verticales se denominan **Aspecto**, que se define en AOP como:
> Modularizaci&oacute;n de una preocupaci&oacute;n que atraviesa m&uacute;ltiples clases.

Como ya estar&aacute; adivinando, un conjunto de varios Aspectos se definen como **Cross Cutting Concern**.

### punto de uni&oacute;n (Joinpoint)

Un punto de uni&oacute;n o Joinpoint se define como:
> Un punto durante la ejecuci&oacute;n de un programa, como la ejecuci&oacute;n de un m&eacute;todo o el manejo de una excepci&oacute;n.

En pocas palabras, en la imagen de arriba, un **Jointpoint** podr&iacute;a ser cualquier m&eacute;todo en la capa empresarial que necesite verificar si el usuario actual tiene el rol o privilegio requerido para permitir su ejecuci&oacute;n. En otras palabras, un Joinpoint es **donde** podemos aplicar un Aspecto.

### Punto de cruce o Pointcut
Hasta ahora hemos identificado dos conceptos, uno de las l&iacute;neas verticales (el Aspecto) y otro de una de nuestras l&iacute;neas horizontales, el m&eacute;todo en la capa de negocio (Jointpoint).
Si interceptamos las l&iacute;neas horizontales y verticales tenemos un **Pointcut**, tiene sentido, ¿verdad?
El punto se define como:
> Un predicado que ayuda a saber d&oacute;nde aplicar un Aspecto en un JoinPoint en particular.

S&eacute; que se est&aacute; complicando un poco. Podemos pensar en Pointcut como una expresi&oacute;n, que en nuestro ser&iacute;a algo como:

> Quiero aplicar el aspecto de seguridad en cualquier m&eacute;todo dentro de la capa empresarial que est&eacute; anotado con la anotaci&oacute;n @Secure

Eso es todo, un predicado, una expresi&oacute;n que ayuda a responder el **d&oacute;nde**. Se ve mejor en la pr&aacute;ctica. Llegaremos a ello m&aacute;s tarde.

### Consejo o Advice
En palabras simples, un **Consejo** es:

> La implementaci&oacute;n de un aspecto, el cual nos interesa aplicar a otros m&oacute;dulos.

O en otras palabras, es la acci&oacute;n a realizar por un aspecto en un Joinpoint particular.
**Qu&eacute;** quieres hacer, en nuestro caso es: "verificar que el usuario tiene el privilegio requerido".
Hay diferentes tipos de **Consejos**, ellos responden a la pregunta de **cu&aacute;ndo**:  

* *Before*: ejecutar el consejo antes de la ejecuci&oacute;n del Jointpoint.
* *After return/After throwing error*: Ejecuta el Consejo despu&eacute;s de la devoluci&oacute;n exitosa o despu&eacute;s de lanzar una excepci&oacute;n.
* *Around*: El Consejo m&aacute;s poderoso. Puede controlar el antes, el despu&eacute;s y el retorno.

> En Spring, Advice se modela como un interceptor, manteniendo una cadena de interceptores alrededor del Joinpoint.

Con estos antecedentes, creemos un ejemplo simple.

## Dependencias
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
````

## Configuraci&oacute;n del proyecto
Cree una aplicaci&oacute;n simple con un Servicio y una Entidad, la ejecutaremos usando CommandLineRunner.

### Entidad cliente
Una clase simple con dos propiedades "nombre" e "id":
````java
public class Customer {

  private String name;
  private int age;

  // getters and setters
}
````

### Capa de servicio
Un componente que tambi&eacute;n act&uacute;a como una fuente de datos, con dos m&eacute;todos **addCustomer** y **getAllCustomers**.
````java
@Service
public class CustomerService {

  private static Logger LOG = LoggerFactory.getLogger(AopCookbookApplication.class);

  private List<Customer> customers;

  public CustomerService() {
    this.customers = new LinkedList<>();
  }

  public Customer addCustomer(Customer newCustomer) {
    LOG.info("Adding new customer: {}", newCustomer.getName());
    this.customers.add(newCustomer);
    return newCustomer;
  }

  public List<Customer> getAllCustomers() {
    LOG.info("Returning all customers");
    return this.customers;
  }

}
````

### el archivo de la aplicaci&oacute;n
Esta es la forma m&aacute;s sencilla de ejecutar una aplicaci&oacute;n con un contexto de Spring, utilizando la interfaz CommandLineRunner:
````java
@SpringBootApplication
public class AopCookbookApplication implements CommandLineRunner {

  private static Logger LOG = LoggerFactory.getLogger(AopCookbookApplication.class);

  @Autowired
  private CustomerService customerService;

  public static void main(String[] args) {
    SpringApplication.run(AopCookbookApplication.class, args);
  }

  @Override
  public void run(String... args) throws Exception {
    LOG.info("EXECUTING : command line runner");
    Customer newCustomer = new Customer();
    newCustomer.setName("My Refactor");
    this.customerService.addCustomer(newCustomer);
    // return customers
    List<Customer> customers = this.customerService.getAllCustomers();
    for (Customer c : customers) {
      LOG.info("Found customer: {}", c.getName());
    }
  }
}
````
Por favor, observe c&oacute;mo dentro del m&eacute;todo **run** estamos llamando a los m&eacute;todos **addCustomer** y **getAllCustomers()** de la clase CustomerService. Estos dos m&eacute;todos son nuestros Aspectos.  

## Aplicando los consejos (Advice)
Supongamos que queremos interceptar todos los m&eacute;todos en CustomerService solo para fines de registro, esto nos lleva a:  

1. El Aspecto es: la funcionalidad de "Logging".
2. El Jointpoint es: la capa de servicio, concretamente "CustomerService".
3. El Pointcut es: "Todos los m&eacute;todos dentro de CustomerService".
4. El Consejo es: el c&oacute;digo real que escribimos para cumplir con el Aspecto, registrando en logs cuando se ejecuta cualquier m&eacute;todo en CustomerService.
5. Finalmente, el tipo de Consejo ser&aacute; **Around**, para el prop&oacute;sito de este tutorial.

### Implementaci&oacute;n de Consejos o Advices
Cree una clase con el nombre "CustomerServiceAdviceExecution", este es el contenido:
````java
@Component
@Aspect
public class CustomerServiceAdviceExecution {

  private static Logger LOG = LoggerFactory.getLogger(CustomerServiceAdviceExecution.class);

  /*
   * Matches all methods inside CustomerService in disregards their signature.
   * 
   * First wildcard refer to any return type, the second refers to any method name and (..) to any
   * parameters.
   */
  @Pointcut(value = "execution(* com.myrefactor.aop.aopcookbook.service.CustomerService.*(..))")
  private void pointcutAllService() {}

  @Around(value = "pointcutAllService()")
  public void aroundAllCustomerService(ProceedingJoinPoint jp) throws Throwable {
    LOG.info("Executing advise BEFORE {} method", jp.getSignature().getName());
    try {
      jp.proceed();
    } finally {
    }
    LOG.info("Executing advise AFTER {} method", jp.getSignature().getName());
  }

}
````
Las cosas importantes a las que hay que prestar atenci&oacute;n son:  

* El uso de la anotaci&oacute;n @Aspect, indicando que esta clase es un aspecto.
* Declaramos un Pointcut con la anotaci&oacute;n @Pointcut. Lea el comentario para entender la expresi&oacute;n.
* Anotamos un m&eacute;todo (la acci&oacute;n a realizar) con @Around y especificamos el Pointcut.
* El par&aacute;metro del m&eacute;todo **aroundAllCustomerService** es el Jointpont real: "ProceedingJoinPoint jp" (El m&eacute;todo en ejecuci&oacute;n). 

### Executing the application
Una vez que ejecute la aplicaci&oacute;n, la salida deber&iacute;a ser similar a esta:
````commandline
c.m.a.a.AopCookbookApplication           : EXECUTING : command line runner
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise BEFORE addCustomer method
c.m.a.a.AopCookbookApplication           : Adding new customer: My Refactor
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise AFTER addCustomer method
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise BEFORE getAllCustomers method
c.m.a.a.AopCookbookApplication           : Returning all customers
c.m.a.a.a.CustomerServiceAdviceWithin    : Executing advise AFTER getAllCustomers method
c.m.a.a.AopCookbookApplication           : Found customer: My Refactor
````
¡Voila! Estamos produciendo logging antes y despu&eacute;s de la ejecuci&oacute;n de cada m&eacute;todo dentro del Servicio al Cliente.

## Conclusion
Hemos cubierto los conceptos principales de AOP y aplicado este conocimiento creando una aplicaci&oacute;n simple que puede interceptar la ejecuci&oacute;n de m&eacute;todos basados en predicados o expresiones.
