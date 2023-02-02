## Poster
![Project Structure](https://drive.google.com/uc?id=1v8gSY2EchU_R73c9IZWHGugxlWwmA86r) 

## Introducción
Escribir aplicaciones de línea de comandos usando Spring es cada vez más necesario para automatizar tareas en el desarrollo de aplicaciones Java. Si bien Spring es un marco de aplicación completo, las bibliotecas como PicoCLI están especializadas en la creación de aplicaciones de línea de comandos. 

En este blog, discutiremos las características clave y los beneficios de usar PicoCLI dentro del marco Spring y comprenderemos cómo se complementan entre sí para crear aplicaciones CLI sólidas y fáciles de usar.

## ¿Qué es un CLI?
Una interfaz de línea de comandos (CLI) es una interfaz de usuario (UI) basada en texto que se utiliza para ejecutar programas, administrar archivos de computadora e interactuar con la computadora. Las interfaces de línea de comandos también se denominan interfaces de usuario de línea de comandos, interfaces de usuario de consola e interfaces de usuario de caracteres.
Las CLI aceptan como comandos de entrada que se ingresan por teclado; los comandos invocados en el símbolo del sistema luego son ejecutados por la computadora.

## ¿Qué es PicoCLI?
Picocli es un marco de trabajo de un solo archivo para crear aplicaciones CLI usando Java con código casi nulo. Picocli pretende ser la forma más fácil de crear aplicaciones de línea de comandos enriquecidas que puedan ejecutarse dentro y fuera de la JVM.

## Using Command Line Runner
CommandLineRunner es una interfaz Spring Boot simple con un método de ejecución. Spring Boot llamará automáticamente al método de ejecución de todos los beans que implementan esta interfaz después de que se haya cargado el contexto de la aplicación.
Aunque puede crear una CLI usando CommandLineRunner, el costo de analizar, mantener y agregar nuevas opciones o subcomandos es alto; por otro lado, el desarrollador debe cuidar cada parámetro y valor. Con PicoCli, la opción y su valor se analizan automáticamente y están disponibles para su uso.

## La aplicación Spring
Para crear una aplicación CLI simple usando Spring y PicoCli, necesitamos básicamente tres componentes:
* Archivo de aplicación Spring Boot: este archivo es común para todas las aplicaciones SpringBoot.
* Un Runner: Un CommandLineRunner que se utilizará como puente para pasar todos los parámetros, opciones y valores al comando de PicoCli.
* Un comando de PicoCli: Este es nuestro comando real, tiene opciones, subcomandos y valores.

El archivo de la aplicación se parece a cualquier otro que haya visto antes:

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PicocliApplication {

	public static void main(String[] args) {
		SpringApplication.run(PicocliApplication.class, args);
	}

}
```

### El ejecutor de la línea de comandos
Crea otro archivo y llámalo `Runner`, dentro pega este contenido:

```java
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.ExitCodeGenerator;
import org.springframework.stereotype.Component;
import picocli.CommandLine;
import picocli.CommandLine.IFactory;

@Component
public class Runner implements CommandLineRunner, ExitCodeGenerator {

  // auto-configured to inject PicocliSpringFactory
  private final IFactory factory;

  private final Command myCommand;

  private int exitCode;

  public Runner(IFactory factory, Command myCommand) {
    this.factory = factory;
    this.myCommand = myCommand;
  }

  @Override
  public void run(String... args) throws Exception {
    exitCode = new CommandLine(myCommand, factory).execute(args);
  }

  @Override
  public int getExitCode() {
    return exitCode;
  }
}
```
Repasemos el código anterior:

1. Lo primero que debemos notar es que es un componente Spring, por lo que usamos **@Controller**.
2. Luego hacemos que esta clase implemente **CommandLineRunner**, por lo que especificamos Spring como una aplicación de línea de comandos.
3. También implementamos **ExitCodeGenerator**. La mayoría de las aplicaciones CLI devuelven códigos, básicamente, si CLI devuelve 0 significa que la ejecución fue correcta y 1 cuando ocurre un error inesperado.
4. Hemos declarado una fábrica: "IFactory", esto viene muy bien desde PicoCli para enlazar opciones y valores.
5. Hemos declarado también un comando: "myCommand" del tipo "Command", y lo implementaremos en el siguiente paso.
6. Finalmente, dentro del método de ejecución, hemos creado un nuevo comando y le hemos dicho que se ejecute pasando todos los argumentos recibidos.

### Escribiendo el comando

Ahora vamos a implementar nuestro comando real y crear un nuevo archivo, lo llamé "Comando", el contenido es:

```java
import java.util.concurrent.Callable;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import picocli.CommandLine;
import picocli.CommandLine.Option;

@Component
@CommandLine.Command(name = "MyRefactorCLI", mixinStandardHelpOptions = true, version = "myrefactor-cli-1.0", description = "CLI Project")
public class Command implements Callable<Integer> {

  @Option(names = { "-a",
      "--address" }, paramLabel = "API_ADDRESS", description = "The address you want to connect to")
  String option;

  private RestTemplate restTemplate = new RestTemplate();

  @Override
  public Integer call() throws Exception {
    System.out.println("Executing option -a: " + this.option);
    return 0;
  }

}
```

Dividiendo el código anterior, esto es lo que necesitamos saber:

1. Usamos la anotación **@CommandLine.Command** de PicoCli y especificamos varios parámetros como el nombre, la descripción y la versión del comando.
2. Hemos declarado un atributo y lo hemos anotado usando **@Option**, hemos especificado el nombre y la descripción de la opción, y ahora veremos cómo podemos usar nuestra CLI.
3. Finalmente, dentro del método **call()**, implementamos la lógica, en este caso, solo imprime el valor de la opción `a/address`.

## Compilando y ejecutando
Necesitamos compilar nuestra aplicación en un archivo `jar` ejecutable, para hacerlo, ejecute el siguiente comando dentro de la carpeta del proyecto:
```commandline
mvn clean install
```

Si tiene éxito, verá un resultado similar a este:

```commandline
------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  10.878 s
[INFO] Finished at: 2022-05-04T17:23:15+03:00
[INFO] ------------------------------------------------------------------------
```
Esto significa que el proyecto ha sido compilado en un archivo **jar**, ubicado dentro de la carpeta "objetivo". En la siguiente imagen se muestra la estructura del proyecto y el archivo `jar` compilado resultante: 

![Estructura del proyecto](https://drive.google.com/uc?id=1DfB0SB0T33HjrMtT5EPwWEEtKK7twzRM) 

En mi caso, el nombre del archivo es: `picocli-0.0.1-SNAPSHOT.jar`. Ejecutemos el archivo usando las opciones indicadas por PicoCli: 

```commandline
java -jar .\target\picocli-0.0.1-SNAPSHOT.jar -a 10.0.0.0
```

Y la salida es la siguiente:

```commandline
...
Executing option -a: 10.0.0.0
...
```

Alternativamente, si intenta especificar una opción no declarada en el `Comando`, automáticamente PicoCli mostrará las instrucciones de uso, por ejemplo, ejecutemos: 

```commandline
java -jar .\target\picocli-0.0.1-SNAPSHOT.jar -h no_defined_option
```

Dado que `h` no es una opción definida, obtendremos:

```commandline
Unknown options: '-h', 'no_defined_otion'
Usage: MyRefactorCLI [-a=API_ADDRESS]
CLI Project
  -a, --address=API_ADDRESS
         The address you want to connect to
```
Y así es como funcionan las anotaciones **@Command** y **@Option**.

## Conclusión:
Spring y PicoCLI son herramientas esenciales para el desarrollo de aplicaciones Java. Spring proporciona un marco completo para crear aplicaciones a gran escala, mientras que PicoCLI proporciona una forma flexible e intuitiva de crear aplicaciones de línea de comandos. Al combinar estas tecnologías, puede crear aplicaciones CLI, ya sea un script simple o una aplicación empresarial a gran escala.
