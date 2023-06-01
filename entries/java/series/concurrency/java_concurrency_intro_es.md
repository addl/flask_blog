## poster
![Object Usage over time in JVMs](https://drive.google.com/uc?id=1Dj534IlTJhUDy6wAQGGFB9xuRcrSNVmA)

## Introducción
Multithreading es un concepto fundamental en la programación de Java que permite la ejecución, al mismo tiempo, de múltiples hilos.
Para una aplicación concurrente, tenemos que crear diferentes hilos de ejecución que se ejecuten en paralelo. En Java existen dos formas básicas de crear hilos de ejecución, la primera es extendiendo la clase Thread y la segunda implementando la interfaz Runnable.

En este artículo, nos enfocaremos en la clase Thread y exploraremos sus propiedades y métodos para crear y ejecutar hilos en Java.

## Fondo
Lo primero que debemos tener en cuenta es que todos los programas Java tienen al menos un 'Hilo', se llama hilo 'principal' y comienza a ejecutarse cuando invocamos el método 'main' de la clase raíz en nuestra aplicación:

````java
public class MyApplication {
	public static void main(String[] args) {
		// our code
	}
}
````

Este es el único hilo en aplicaciones **no concurrentes** y el primero en **aplicaciones concurrentes**.

## La clase Thread
La clase Thread en Java representa un hilo de ejecución. Proporciona funcionalidades y operaciones esenciales para controlar y administrar hilos.
Para crear un hilo, solo necesitamos extender la clase Thread e implementar su método `run`:

````java
public class MyThread extends Thread {
    public void run() {
        // Code to be executed in the thread
    }
}
````

## Un hilo personalizado en acción
Para demostrar cómo funcionan los subprocesos o hilos, creemos una aplicación simple con un hilo personalizado.

````java
public class MyThread extends Thread {

  @Override
  public void run() {
    Thread theThread = currentThread();
    try {
      theThread.sleep(1000);
      System.out.println("My thread with ID: " + theThread.getId());
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
  
}
````
En el código de arriba:
1. Creamos una clase `MyThread` que extiende la clase `Thread` e implementamos el método **run**. 
2. Obtenemos la instancia del hilo usando **currentThread()**. Este método es un método estático de la clase Thread que devuelve una instancia del 'Thread' actual. 
3. Luego imprimimos un mensaje para identificar nuestro Thread con su ID único, obtenemos el ID llamando al método **getId()** de la clase `Thread`. 

Ahora necesitaremos un hilo principal para ejecutar nuestra aplicación:
````java
public class Main {
  public static void main(String[] args) {
    Thread mainThread = Thread.currentThread();
    MyThread myThread = new MyThread();
    myThread.start();
    System.out.println("The Main Thread with ID: " + mainThread.getId());
  }
}
````
Arriba hicimos lo siguiente:
1. En la primera línea, la variable `mainThread` contiene una referencia al hilo que se está ejecutando actualmente, que es el **hilo principal del programa**. 
2. La siguiente línea crea una instancia de la clase `MyThread`. Esto crea un nuevo objeto del hilo pero **aún no inicia su ejecución**. 
3. Para crear un nuevo hilo de ejecución llamamos al método **start()** desde una instancia de la clase Thread: `myThread.start();`.

Al ejecutar el programa, obtenemos algo similar a esto:
````commandline
The Main Thread with ID: 1
My thread with ID: 23
````

Notarás como la segunda línea tarda un poco más (1000ms = 1seg) en mostrarse en la consola. Observe también cómo el hilo principal no se interrumpe llamando al método **start** de `myThread` y continúa con su ejecución, sin esperar la ejecución de `myThread`.
> En Java, los ID de subprocesos dependen del sistema y no se garantiza que sus valores sean consecutivos.

Ahora que vemos en acción cómo crear hilos, profundicemos en más detalles.

## Tipos de hilo
En Java, los subprocesos o hilos se pueden clasificar en dos tipos según su comportamiento y su impacto en **la terminación del programa**: subprocesos `daemon` y subprocesos `no-daemon`.

### Subprocesos Daemon:
* Se ejecutan en segundo plano para realizar tareas que **no necesariamente deben completarse** antes de que finalice el programa. 
* La JVM **no esperará** a que se complete ningún subproceso daemon antes de finalizar el programa. 
* Por lo general, se utilizan para tareas como la recolección de basura, la monitorización u otras actividades de mantenimiento que pueden ejecutarse de forma independiente, sin afectar la funcionalidad principal del programa. 


### Subprocesos No Daemon:
* Son hilos de usuario creados explícitamente por el programa y que realizan tareas críticas para la funcionalidad del programa. 
* La JVM **espera a todos los subprocesos que no sean daemon** hasta completar su ejecución, para después finalizar el programa. 
* Son esenciales para la ejecución de la lógica principal del programa y **deben completar sus tareas** antes de que finalice el programa. 

En resumen, la distinción entre subprocesos daemon y no daemon en Java está relacionada principalmente con el comportamiento de la JVM al finalizar el programa.
Para notar la diferencia, hagamos que nuestro subproceso personalizado sea un demonio(daemon):

````java
public static void main(String[] args) {
    Thread mainThread = Thread.currentThread();
    MyThread myThread = new MyThread();
    myThread.setDaemon(true);
    myThread.start();
    System.out.println("The Main Thread with ID: " + mainThread.getId());
  }
````
Después de ejecutar el programa, la salida es:
````commandline
The Main Thread with ID: 1
````

Observe cómo la JVM finaliza el subproceso principal **sin esperar** a que finalice nuestro hilo personalizado.
> Debemos establecer el daemon como `true` antes de llamar al método **start**.

## Prioridad en los hilos
Todos los hilos en Java tienen prioridad, es un valor entero de 0 (Thread.MIN_PRIORITY) a 10 (Thread.MAX_PRIORITY). De forma predeterminada, los hilos son creados con prioridad 5 (Thread.NORM_PRIORITY).

La prioridad es una pista para la JVM y el sistema operativo sobre qué subprocesos son "preferibles", pero no hay garantía del orden de ejecución, ya que no significa un contrato y, por tanto, no es obligatorio que un hilo con más prioridad se ejecute primero que uno con prioridad más baja.

## Estado del hilo
Un hilo puede tener varios estados a lo largo de su ciclo de vida:

1. New: el subproceso se encuentra en el nuevo estado cuando se crea, pero aún no se ha iniciado. 
2. Runnable: en el estado ejecutable, el subproceso puede ejecutarse y el sistema operativo subyacente le asignará tiempo de CPU siempre que sea posible. 
3. Blocked/Waiting: un subproceso puede entrar en un estado bloqueado o de espera cuando está esperando un desbloqueo o esperando que se cumpla una condición específica antes de poder continuar. 
4. Timed Waiting: similar al estado **Blocked/Waiting**, pero tiene un tiempo limite de espera.
6. Terminated: el subproceso alcanza el estado terminado cuando se completa su ejecución.


## Métodos en la clase Thread
La clase `Thread` tiene métodos que permiten a los desarrolladores obtener y cambiar información:

1. **start()**: Inicia la ejecución del subproceso e invoca al sistema operativo para asignar recursos para el subproceso.
2. **run()**: Contiene el código que será ejecutado por el hilo. 
3. **getId()**: Devuelve el identificador único asignado al hilo. 
4. **getName()** y **setName(String name)**: getName() recupera el nombre del hilo, mientras que setName(String name) establece un nuevo nombre para el hilo. 
5. **sleep(long millis)**: pausa la ejecución del subproceso actual durante el número especificado de milisegundos. 
6. **join()**: espera a que el hilo en el que se llama a este método complete su ejecución. 
7. **interrupt()**: Interrumpe la ejecución de un subproceso estableciendo su estado de interrupción. 
8. **isInterrupted()**: Comprueba si el hilo actual ha sido interrumpido. 
9. **rendimiento()**: Sugiere que el subproceso que se está ejecutando actualmente renuncia voluntariamente a la CPU para permitir que se ejecuten otros subprocesos. 
10. **getPriority()** y **setPriority(int priority)**: Obtiene o establece la prioridad del hilo. 
11. **isAlive()**: Comprueba si el subproceso se está ejecutando actualmente o ha finalizado. 

## Conclusiones
La clase Thread es un componente crucial en la concurrencia y multithreading de Java. Proporciona las funcionalidades básicas para crear, iniciar y administrar subprocesos en Java.
En este artículo, hablamos sobre la clase Thread y creamos una aplicación simple para comprender cómo funciona la concurrencia y ejecución de subprocesos múltiples.
En la próxima publicación de esta serie, implementaremos un problema clásico de Productor y Consumidor utilizando el conocimiento que hemos aprendido aquí.
