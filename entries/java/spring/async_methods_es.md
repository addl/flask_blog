## poster
![Async Spring Annotation](https://drive.google.com/uc?export=view&id=1zmNosZVzpZjjnx74xz3lgfXQePV4JToX)

## Introducción
En una aplicación web, es común realizar tareas de larga duración, como enviar correos electrónicos o procesar grandes cantidades de datos. Estas tareas pueden tardar mucho tiempo en completarse y pueden bloquear el subproceso que las ejecuta, lo que genera un rendimiento deficiente y una experiencia de usuario lenta.

En las aplicaciones de Spring, podríamos usar la anotación `@Async` para ejecutar tales tareas de forma asincrónica, lo que permite que el subproceso principal continúe procesando otras solicitudes mientras la tarea se ejecuta en segundo plano. En esta publicación de blog, discutiremos cómo usar la anotación `@Async` con un bean ejecutor de subprocesos en Spring.

## La anotación @Async
La anotación `@Async` se puede aplicar a un método para indicar que debe ejecutarse de forma asíncrona. Cuando se anota un método con `@Async`, se ejecutará en un subproceso separado, lo que permitirá que el subproceso principal continúe procesando otras solicitudes. Aquí hay un ejemplo de un método que envía un correo electrónico de forma asíncrona:
````java
@Service
public class AsyncService {

    @Async
    public void sendEmail(String to, String subject, String body) {
        // code to send email
    }
}
````
En el ejemplo anterior, el método **sendEmail** está anotado con `@Async`, por lo que se ejecutará en un subproceso separado cuando se le llame. El método anotado con `@Async` está representado por Spring y, por lo tanto, hay un par de cosas que debe tener en cuenta:
1. Debe aplicarse solo a **métodos públicos**.
2. La autoinvocación no funcionará
> **Autoinvocación** se refiere a la acción de llamar a un método desde el mismo bean, o sea dentro de la misma clase.

## Uso de un bean ejecutor de subprocesos
La anotación `@Async` le dice a Spring que ejecute un método de forma asíncrona, pero no especifica cómo se debe ejecutar el método. De forma predeterminada, Spring usará `SimpleAsyncTaskExecutor` para ejecutar métodos asíncronos, lo que crea un nuevo hilo para cada llamada de método. Sin embargo, esto puede ser un problema si su aplicación realiza una gran cantidad de llamadas a métodos asincrónicos, ya que puede provocar problemas de rendimiento y escasez de recursos.

Podemos configurar nuestro propio bean ejecutor de subprocesos y especificarlo para que se use con la anotación `@Async`. He aquí un ejemplo de cómo hacer esto:

````java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

  @Value("${myrefactor.core.pool.size}")
  public int corePoolSize;

  @Value("${myrefactor.max.pool.size}")
  public int maxPoolSize;

  @Bean(name = "threadPoolTaskExecutor")
  public Executor threadPoolTaskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(corePoolSize);
    executor.setMaxPoolSize(maxPoolSize);
    executor.setThreadNamePrefix("task_executor_thread");
    executor.initialize();
    return executor;
  }

  @Override
  public Executor getAsyncExecutor() {
    return threadPoolTaskExecutor();
  }

}
````
En este ejemplo, hemos creado un bean llamado **threadPoolTaskExecutor** de tipo `ThreadPoolTaskExecutor`. Este es un ejecutor de grupo de subprocesos proporcionado por Spring que nos permite configurar la cantidad de subprocesos en el grupo y otros parámetros.
Luego tenemos la clase `AsyncConfig` que implementa `AsyncConfigurer` y, al hacerlo, esta configuración es global y se aplica a todos los métodos anotados `@Async`. La clase `AsyncConfigurer` tiene un método `getAsyncExecutor` que sobreescribimos y devuelve nuestro bean configurado.

> Si desea configurar `@Async` a nivel de método, simplemente no implemente la interfaz `AsyncConfigurer` y use `@Async` especificando el nombre del bean ejecutor de la tarea: `@Async("threadPoolTaskExecutor")`.

## Comprendiendo la configuración del ejecutor de subprocesos
Como habrá notado anteriormente, la clase `ThreadPoolTaskExecutor` en Spring proporciona varios métodos para configurar el grupo de subprocesos, incluidos **setCorePoolSize()** y **setMaxPoolSize()**.

### Core pool size
El método **setCorePoolSize()** establece la cantidad de subprocesos que deben estar siempre activos en el grupo de subprocesos. Esto significa que si no hay tareas para ejecutar, esta cantidad de subprocesos se ejecutará y esperará nuevas tareas. Por ejemplo, si establece este valor a 4, siempre habrá 4 subprocesos ejecutándose en el grupo de subprocesos, incluso si no hay tareas para ejecutar.

### Max pool size
El método **setMaxPoolSize()** establece el número máximo de subprocesos que se pueden crear en el grupo de subprocesos. Esto significa que si hay más tareas para ejecutar que subprocesos disponibles en el grupo, se crearán subprocesos adicionales hasta este límite. Por ejemplo, si establece el tamaño máximo del grupo en 8 y tiene 10 tareas para ejecutar, se crearán 8 subprocesos para ejecutar las tareas y se colocarán dos tareas en la cola.

### Tamaño de la cola
Puede usar el método **setQueueCapacity()** para configurar el tamaño de la cola y controlar cuántas tareas pueden estar esperando para ser ejecutadas. Cuando el grupo de subprocesos está lleno (no hay subprocesos disponibles) y se envía una nueva tarea, se agregará a la cola si todavía hay espacio disponible. Si la cola está llena y se envía una nueva tarea, se rechazará y se generará una `RejectedExecutionException`.

### Prioridad de subproceso
El método **setThreadPriority()** le permite establecer la prioridad de los subprocesos en el grupo de subprocesos. Este método toma un entero como argumento, que debería ser una de las constantes de prioridad definidas en la clase `Thread`.

Las constantes de prioridad posibles para el método setThreadPriority son:
* Thread.MIN_PRIORITY (una constante con valor 1), la prioridad más baja
* Thread.NORM_PRIORITY (una constante con valor 5) la prioridad por defecto
* Thread.MAX_PRIORITY (una constante con valor 10) la prioridad más alta

## Manejo de valores devueltos
Cuando se usa la anotación @Async para ejecutar un método de forma asíncrona, el subproceso de llamada no esperará a que se complete el método asíncrono y seguirá ejecutando su propio código. Para manejar los valores devueltos por un método asíncrono, tiene varias opciones:

### Usando el objeto `Futuro`
Al llamar al método **get()** en el objeto `Future`, **bloqueará el subproceso de llamada** hasta que se complete el método asíncrono. También puede usar el método **get(long timeout, TimeUnit unit)** para especificar un tiempo de espera para la llamada. El método **get()** devolverá el resultado del método asíncrono si la ejecución es exitosa o lanzará una `ExecutionException` si el método asíncrono lanzó una excepción.

````java
@Async
public Future<String> asyncMethodWithReturnType() {
    return new AsyncResult<>("someValue");
}
...
try {
    String result = asyncMethodWithReturnType().get();
    // do something with result
} catch (InterruptedException | ExecutionException e) {
    // handle exception
}
...
````

### Usando `ListenableFuture` o `CompletableFuture`

Al usar `ListenableFuture<T>` o `CompletableFuture<T>` en lugar de `Future<T>`, agrega devoluciones de llamada, que se ejecutarán una vez que se complete la tarea asíncrona. De esta manera, puede continuar procesando en el subproceso de llamada sin tener que esperar a que se complete la tarea asíncrona.

````java
@Async
public ListenableFuture<String> asyncMethodWithListenableFuture(){
    return new AsyncResult<>("someValue");
}

...
ListenableFuture<String> listenableFuture = asyncMethodWithListenableFuture();
listenableFuture.addCallback(
    result -> {
        // handle success
    });
...
````

### Uso de la interfaz `Callback`

Puede pasar una interfaz de devolución de llamada como argumento al método asíncrono. La interfaz de devolución de llamada debe tener un solo método para manejar el resultado del método asíncrono, que será invocado por el método asíncrono una vez que se complete.

````java
interface Callback{
    void handle(String result);
}

@Async
public void asyncMethodWithCallback(Callback callback){
    callback.handle("someValue");
}

...
asyncMethodWithCallback(result -> {
   //handle the result
});
...
````

> `ListenableFuture<T>` o `CompletableFuture<T>` proporciona una gran cantidad de funciones listas para usar, como el encadenamiento y el manejo de excepciones.

## Manejo de excepciones
Cuando se usa la anotación @Async para ejecutar un método de forma asíncrona, es importante manejar cualquier excepción que pueda ocurrir dentro del método, ya que no se propagará al subproceso de llamada.

Hay varias formas de manejar las excepciones cuando se usa la anotación `@Async`, según sus requisitos específicos:

### Usando `Future`
Si opta por usar `Future` como en el tema anterior, simplemente use try-catch de la siguiente manera:

`````java
try {
    String result = asyncMethodWithReturnType().get();
    // do something with result
} catch (InterruptedException | ExecutionException e) {
    // handle exception
}
`````

### Usando `ListenableFuture` o `CompletableFuture`
Este enfoque nos permite registrar devoluciones de llamadas y manejar excepciones de una manera más elegante.

````java
@Async
public ListenableFuture<String> asyncMethodWithListenableFuture(){
    return new AsyncResult<>("someValue");
}

...
ListenableFuture<String> listenableFuture = asyncMethodWithListenableFuture();
listenableFuture.addCallback(
    result -> {
        // handle success
    },
    ex -> {
        // handle exception
    });
...
````

### Using `AsyncUncaughtExceptionHandler`

This interface has a single method, **handleUncaughtException(Throwable ex, Method method, Object... params)** that will be called by Spring when an exception is thrown by an async method.
Here is an example, create a class implementing this interface:
````java
class CustomAsyncExceptionHandler implements AsyncUncaughtExceptionHandler {
    @Override
    public void handleUncaughtException(Throwable ex, Method method, Object... params) {
        log.error("{} threw exception: {} ", Thread.currentThread().getName(), throwable.getMessage());
        log.error("Method name: {} ", method.getName());
        log.error("With params: ");
        for (Object param : params) {
          log.error("Param value: {} ", param);
        }
    }
}
````

El código anterior registrará toda la información posible sobre la excepción. Ahora ampliaremos nuestra configuración en `AsyncConfig` sobreescribiendo un nuevo método:
````java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

  ...

  @Override
  public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
    return new CustomAsyncExceptionHandler();
  }
}
````
En particular, prefiero esta opción, ya que puede usar un `AsyncUncaughtExceptionHandler` para implementar una estrategia global de manejo de excepciones para su aplicación, como registrar la excepción o enviar una notificación por correo electrónico.

# Conclusión
En esta publicación de blog, hemos discutido cómo usar la anotación Spring `@Async` para ejecutar métodos de forma asincrónica y cómo usar y configurar un bean ejecutor de subprocesos para administrar los subprocesos utilizados por los métodos asincrónicos.
También cubrimos cómo manejar excepciones y recibir valores devueltos de métodos asincrónicos. Aplicando estos consejos podemos mejorar el rendimiento y la capacidad de respuesta de nuestra aplicación y evitar bloquear el hilo principal mientras se ejecutan tareas de larga duración.

¡Feliz código!