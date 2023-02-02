## Poster
![Project Structure](https://drive.google.com/uc?id=1v8gSY2EchU_R73c9IZWHGugxlWwmA86r) 

## Introduction
Writing command line applications using Spring is increasingly necessary to automate tasks in Java application development. While Spring is a full-fledged application framework, libraries like PicoCLI are specialized in building command-line applications. In this blog, we will discuss the key features and benefits of using PicoCLI within Spring framework and understand how they complement each other in building robust and user-friendly CLI applications.

## What is a CLI application?
A command-line interface (CLI) is a text-based user interface (UI) used to run programs, manage computer files and interact with the computer. Command-line interfaces are also called command-line user interfaces, console user interfaces and character user interfaces. 
CLIs accept as input commands that are entered by keyboard; the commands invoked at the command prompt are then run by the computer.

## What is PicoCLI
Picocli is a one-file framework for creating CLIs applications using Java with almost zero code. Picocli aims to be the easiest way to create rich command line applications that can run on and off the JVM.

## Spring's Command Line Runner
CommandLineRunner is a simple Spring Boot interface with a run method. Spring Boot will automatically call the run method of all beans implementing this interface after the application context has been loaded.  
Although you can create a CLIs using CommandLineRunner, the cost to parse, maintain and adding new options or subcommands is high, on the other hand the developer should take care of every single parameter and values. With PicoCli the option and its value is automatically parsed and available for use.

## The Spring application
To create a simple CLI application using Spring and PicoCli we need basically three components:  
* Spring Boot application file: This file is common for all SpringBoot applications.
* A Runner: A CommandLineRunner that will be used as a bridge to pass all parameters, options and values to PicoCli's command.
* A PicoCli's command: This is our actual command, having options, subcommands and values.

The application file looks like any other you might have seen before:
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

### The command line runner
Create another file and call it `Runner`, inside paste this content:

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
Let's go through the above code:  

1. The first thing we need to notice is that it is a Spring component, so we used **@Controller**.  
2. Then we make this class to implement **CommandLineRunner**, thus we specify Spring as a command line application.  
3. We also implement **ExitCodeGenerator**. Most CLI applications return codes, basically, if CLI returns 0 means that the execution was ok, and 1 when an unexpected error occurs.
4. We have declared a factory: "IFactory", this comes in handy from PicoCli to bind options and values.
5. We have declared also a command: "myCommand" of the "Command" type, and we will implement it in the next step.
6. Finally, inside the run method, we have created a new command and told it to execute by passing all arguments received.

### Writing the command

Now we are going to implement our actual command and create a new file, I called it "Command", the content is: 

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

Splitting up the above code, this is what we need to know:  

1. We have used the annotation **@CommandLine.Command** from PicoCli and specified several parameters like the name, description, and version of the command
2. We have declared an attribute and annotated it using **@Option**, we have specified the option's name and description, and we will see now how we can use our CLI.
3. Finally, inside the **call()** method, we implement out logic, in this case, it just prints the value of the `a/address` option.

## Compiling and running
We need to compile our application into an executable `jar` file, to do so, run the following command inside the project's folder: 

```commandline
mvn clean install
```

If it succeeds, you will see an output similar to this one:
```commandline
------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  10.878 s
[INFO] Finished at: 2022-05-04T17:23:15+03:00
[INFO] ------------------------------------------------------------------------
```
This means the project has been compiled into a **jar** file, located inside the "target" folder, In the following picture is the project structure and the resulting compiled `jar` file: 

![Project Structure](https://drive.google.com/uc?id=1DfB0SB0T33HjrMtT5EPwWEEtKK7twzRM) 

In my case, the filename is: `picocli-0.0.1-SNAPSHOT.jar`. Let's execute the file by using the options indicates by PicoCli:

```commandline
java -jar .\target\picocli-0.0.1-SNAPSHOT.jar -a 10.0.0.0
```

And the output is the following:

```commandline
...
Executing option -a: 10.0.0.0
...
```

Alternatively if you try to specify an option not declared in the `Command`, automatically PicoCli will show the usage instructions, for instance, let's execute: 

```commandline
java -jar .\target\picocli-0.0.1-SNAPSHOT.jar -h no_defined_option
```

Since `h` is not a defined option, we will get:

```commandline
Unknown options: '-h', 'no_defined_otion'
Usage: MyRefactorCLI [-a=API_ADDRESS]
CLI Project
  -a, --address=API_ADDRESS
         The address you want to connect to
```
And this is how the **@Command** and **@Option** annotations work. 

## Conclusion:
Spring and PicoCLI are essential tools for Java application development. Spring provides a comprehensive framework for building large-scale applications, while PicoCLI provides a flexible and intuitive way to build command-line applications. By combining these technologies you can build CLI applications either a simple script or a large-scale enterprise application.
