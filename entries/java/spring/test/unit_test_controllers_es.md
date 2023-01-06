## Introduction
En esta entrada aprenderemos a usar Spring Framework y Mockito para brindar cobertura de prueba a la capa del controlador usando Rest y JSON.

## Requirements
* Maven instalado
* Java 11+
* Spring Boot 2.6+
* Editor de texto, In mi caso IntelliJ

## What is JUnit?
JUnit es un marco de c&oacute;digo abierto de pruebas unitarias para el lenguaje de programaci&oacute;n Java.
Los desarrolladores de Java utilizan este marco para escribir y ejecutar pruebas automatizadas.
En Java, hay casos de prueba que deben volver a ejecutarse cada vez que se agrega un c&oacute;digo nuevo.
Esto se hace para asegurarse de que no se rompa nada en el c&oacute;digo.

## What is Unit Testing?
Las pruebas unitarias, como sugiere el nombre, se refieren a la prueba de peque&ntilde;os segmentos de c&oacute;digo.
Las pruebas unitarias suelen ser pruebas automatizadas escritas y ejecutadas por desarrolladores de software para garantizar que una secci&oacute;n de una aplicaci&oacute;n (conocida como la "unidad") cumpla con su dise&ntilde;o y se comporte seg&uacute;n lo previsto.
En esta publicaci&oacute;n, el segmento de c&oacute;digo que estamos probando es la capa del controlador.

## Dependencies
````xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
````

## Creando el proyecto
Para probar unidades de un sistema, debemos tener al menos un sistema m&iacute;nimo.
Creemos una aplicaci&oacute;n con dos servicios web tipo Rest para almacenar y recuperar usuarios.

### Entidad
Nuestra clase de entidad o modelo es un usuario simple con "nombre" e "id".
````java
public class User {

  private UUID id;
  private String name;

  // getters and setter

}
````

### Capa de servicio
Estamos creando un componente de servicio que ser&aacute; utilizado por nuestros controladores.
````java
@Service
public class UserService {

  private List<User> userDataSource;

  public UserService(){
    userDataSource = new LinkedList<>();
  }

  public User addUser(User user){
    user.setId(UUID.randomUUID());
    this.userDataSource.add(user);
    return user;
  }
  
  public List<User> getAllUsers(){
    return userDataSource;
  }

}
````
En el c&oacute;digo anterior, estamos usando una fuente de datos en memoria, una lista simple **userDataSource**.
Proporcionamos dos m&eacute;todos, uno para agregar un nuevo usuario y el otro para obtener todos los usuarios en la base de datos: la lista ;)

### Capa controladora
Esta es la capa que se espera que probemos. Para simplificar, estamos creando un controlador Rest.
````java
@RestController
public class UserController {

  @Autowired
  private UserService userService;

  @PostMapping("/add-user")
  public User submitUser(@RequestBody User newUser){
    User user = userService.addUser(newUser);
    return user;
  }

  @GetMapping("all-users")
  public List<User> getAllUsers(){
    return userService.getAllUsers();
  }

}
````
De manera similar a nuestro servicio, tenemos dos m&eacute;todos, uno para enviar un Usuario y otro para recuperar todos los usuarios en la base de datos.
Observe c&oacute;mo estamos inyectando "userService" como una dependencia.

### Estructure del proyecto
La estructura del proyecto deber&iacute;a verse como esta imagen:  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1-LluwKGqopS1X9bFV0l37qq__M5CZPtq)


## Creando el test
Las pruebas unitarias t&iacute;picas se crean en un directorio separado. La convenci&oacute;n est&aacute;ndar de las herramientas de compilaci&oacute;n de Maven y Gradle es usar:

* src/main/java - para c&oacute;digo
* src/test/java - para pruebas

Dicho esto, cree una clase *UserControllerTest*, consulte la imagen de arriba (Estructura del proyecto), el contenido de la prueba es:
````java
class UserControllerTest {

  private MockMvc mockMvc;

  @InjectMocks
  private UserController lookupController;

  @Mock
  UserService userService;

  /**
   * @throws java.lang.Exception
   */
  @BeforeEach
  public void setUp() throws Exception {
    MockitoAnnotations.openMocks(this);
    this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
  }

  @Test
  void whenSubmitUser_thenUserIdIsGenerated() throws Exception {
    User newUser = new User();
    newUser.setName("My Refactor");

    User result = new User();
    result.setName("My Refactor");
    UUID id = UUID.randomUUID();
    result.setId(id);

    Mockito.when(userService.addUser(Mockito.any(User.class))).thenReturn(result);

    this.mockMvc
        .perform(post("/add-user").content(asJsonString(newUser)).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(notNullValue())))
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(equalTo(id.toString()))))
        .andReturn();
  }

  private static String asJsonString(final Object obj) {
    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.writeValueAsString(obj);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
````
No te preocupes si ahora mismo no tiene mucho sentido, repasemos para entender cada parte.

## Comprendiendo las anotaciones @InjectMocks y @Mock
B&aacute;sicamente usamos estas anotaciones para crear maquetas de los componentes involucrados en la prueba.
Con @InjectMocks creamos una instancia de nuestra clase de controlador e inyectamos en ella las dependencias que ha declarado y que hemos anotado con @Mock.
Dado que anotamos UserService como @Mock, hemos creado un bean de este tipo y, debido a que nuestro controlador tiene una dependencia del mismo tipo. Mockito lo inyectar&aacute;.

## Preparaci&oacute;n del test con @BeforeEach
Antes de ejecutar una prueba, creamos un contexto independiente inicializando los componentes de las maquetas:
````java
@BeforeEach
public void setUp() throws Exception {
    MockitoAnnotations.openMocks(this);
    this.mockMvc = MockMvcBuilders.standaloneSetup(lookupController).build();
}
````
> Tenga en cuenta que si est&aacute; usando JUnit4, la anotaci&oacute;n es @Before y en lugar de **openMocks** debe usar **initMocks**

## Configurando el comportamiento

Una de las ventajas de usar Mockito es que puedes especificar el comportamiento de tus objetos simulados.

````java
...
Mockito.when(userService.addUser(Mockito.any(User.class))).thenReturn(result);
...
````
En este caso, le estamos diciendo al contexto que cuando se invoca el m&eacute;todo **addUser** y su par&aacute;metro es una instancia de la clase **User**, debe devolver un usuario con **id**.

> Esto evita que Mockito compare el argumento con el valor devuelto, lo que a veces conduce a un cuerpo de respuesta vac&iacute;o de los controladores en las pruebas.

## Ejecutando la solicitud y verificando
Hemos llegado a la parte m&aacute;s importante, el c&oacute;digo donde realizamos la petici&oacute;n a nuestro controlador y confirmamos que el comportamiento es el esperado:
````java
...
this.mockMvc
        .perform(post("/add-user").content(asJsonString(newUser)).contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk()).andDo(print())
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(notNullValue())))
        .andExpect(MockMvcResultMatchers.jsonPath("$.id", is(equalTo(id.toString()))));
...
````
Resumiendo:
1. Primero, estamos usando *mockMvc* inicializado en el m&eacute;todo **setUp** para realizar una solicitud.
2. La solicitud es POST a la URL "/add-user" y el tipo de contenido es APPLICATION_JSON (porque nuestro controlador es REST)
3. Usamos ResultActions como **andExpect** y **andDo** en combinaci&oacute;n con **status** de MockMvcResultMatchers y **isOk** de StatusResultMatchers para confirmar que el estado es 200 OK.
4. Finalmente, utilizamos **MockMvcResultMatchers.jsonPath** para leer el JSON en la respuesta y comparar la identificaci&oacute;n del objeto devuelto.

## Ejecutando el test
Para ejecutar la prueba, simplemente haga clic derecho dentro de la clase de prueba de la siguiente manera:  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1lGoNcW3OefO6qcrTYWqhTRh8VnzUweca)

Esta es mi parte favorita, cuando la barra de prueba se vuelve verde :)  

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1Z3pmbhzz8ZoVza6bDb7Ak5jOjqtGAgHv)

Eso es todo, espero que esta entrada te haya sido de utilidad.

## Conclusi&oacute;n
En este art&iacute;culo, hemos resumido los pasos m&aacute;s simples para escribir las pruebas unitarias b&aacute;sicas usando Mockito y Spring Framework.