## poster
![Async Spring Annotation](https://drive.google.com/uc?export=view&id=1zmNosZVzpZjjnx74xz3lgfXQePV4JToX)


## Introduction
In a web application, it's common to perform long-running tasks, such as sending emails or processing large amounts of data. These tasks can take a significant amount of time to complete and can block the thread that is executing them, leading to poor performance and a slow user experience. 

In Spring applications we could use `@Async` annotation to execute such tasks asynchronously, allowing the main thread to continue processing other requests while the task is being executed in the background. In this blog post, we'll discuss how to use the `@Async` annotation with a thread executor bean in Spring.

## The @Async Annotation
The `@Async` annotation can be applied to a method to indicate that it should be executed asynchronously. When a method is annotated with @Async, it will be executed in a separate thread, allowing the main thread to continue processing other requests. Here's an example of a method that sends an email asynchronously:

````java
@Service
public class AsyncService {

    @Async
    public void sendEmail(String to, String subject, String body) {
        // code to send email
    }
}
````
In the above example, the **sendEmail** method is annotated with `@Async`, so it will be executed in a separate thread when called. Method annotated with `@Async` are proxied by Spring and hence there are couple thing you should have in mind:
1. It must be applied to **public methods only**.
2. Self-invocation won't work
> **Self-invocation** refers to the action of calling one method from the same bean, within the same class.

## Using a Thread Executor Bean
The `@Async` annotation tells Spring to execute a method asynchronously, but it doesn't specify how the method should be executed. By default, Spring will use a `SimpleAsyncTaskExecutor` to execute async methods, which creates a new thread for each method call. However, this can be a problem if your application makes a large number of async method calls, as it can lead to resource starvation and performance issues.

We can configure our own thread executor bean and specify it to be used with the `@Async` annotation. Here's an example of how to do this:
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
In this example, we've created a bean called **threadPoolTaskExecutor** of type `ThreadPoolTaskExecutor`. This is a thread pool executor provided by Spring that allows us to configure the number of threads in the pool and other parameters.
We then have `AsyncConfig` class which implements `AsyncConfigurer` and by doing so this configuration is global and applied to all `@Async` annotated methods. `AsyncConfigurer` class has a method `getAsyncExecutor` that we override and returns our configured bean.
> If you want to configure `@Async` at method level, simply don't implement `AsyncConfigurer` interface and use `@Async` by specifying the name of the task executor bean: `@Async("threadPoolTaskExecutor")`.
 
## Understanding Thread Executor Configuration
As you might have noticed above, the `ThreadPoolTaskExecutor` class in Spring provides several methods for configuring the thread pool, including **setCorePoolSize()** and **setMaxPoolSize()**.

### Pool size core
The **setCorePoolSize()** method sets the number of threads that should be always active in the thread pool. This means that if there are no tasks to execute, this number of threads will be running and waiting for new tasks. For example, if you set the core pool size to 4, there will always be 4 threads running in the thread pool, even if there are no tasks to execute.

### Max pool size
The **setMaxPoolSize()** method sets the maximum number of threads that can be created in the thread pool. This means that if there are more tasks to execute than there are available threads in the pool, additional threads will be created up to this limit. For example, if you set the max pool size to 8, and you have 10 tasks to execute, 8 threads will be created to execute the tasks and two task will be placed in the queue.

### Queue size
You can use the **setQueueCapacity()** method to configure the size of the queue and control how many tasks can be waiting to be executed. When the thread pool is full (no threads available) and a new task is submitted, it will be added to the queue if there is still space available. If the queue is full and a new task is submitted, it will be rejected, and a `RejectedExecutionException` will be thrown.

### Thread priority
The **setThreadPriority()** method allows you to set the priority of the threads in the thread pool. This method takes an int as an argument, which should be one of the priority constants defined in the `Thread` class.

The possible priority constants for the setThreadPriority method are:
* Thread.MIN_PRIORITY (a constant with value 1), the lowest priority
* Thread.NORM_PRIORITY (a constant with value 5) the default priority
* Thread.MAX_PRIORITY (a constant with value 10) the highest priority

## Handling returned values
When using the @Async annotation to execute a method asynchronously, the calling thread will not wait for the async method to complete and will continue executing its own code. To handle the values returned by an async method, you have several options:

### Using `Future` object
Calling the **get()** method on the `Future` object, **will block the calling thread** until the async method completes. You can also use the **get(long timeout, TimeUnit unit)** method to specify a timeout for the call. The **get()** method will return the result of the async method if the execution is successful or throw an `ExecutionException` if the async method threw an exception.
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

### Using `ListenableFuture` or `CompletableFuture`

By using `ListenableFuture<T>` or `CompletableFuture<T>` instead of `Future<T>` you add callbacks, which will be executed once the async task is completed. This way, you can continue processing on the calling thread without having to wait for the async task to complete.
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

### Using `Callback` interface

You can pass a callback interface as an argument to the async method. The callback interface should have a single method to handle the result of the async method, which will be invoked by the async method once it completes.
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

> `ListenableFuture<T>` or `CompletableFuture<T>` provides a lot of functionality out of the box, such as chaining and exception handling.

## Exception handling
When using the @Async annotation to execute a method asynchronously, it's important to handle any exceptions that may occur within the method, as they will not be propagated to the calling thread.

There are several ways to handle exceptions when using the `@Async` annotation, depending on your specific requirements:

### Using `Future`
If you opt for using `Future` like in the previous topic, just use try-catch as follow:
`````java
try {
    String result = asyncMethodWithReturnType().get();
    // do something with result
} catch (InterruptedException | ExecutionException e) {
    // handle exception
}
`````

### Using `ListenableFuture` or `CompletableFuture`
This approach allows to register callbacks and handle exception in a more elegant way.
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
The above code will log all possible information about the exception. Now we will extend our configuration in `AsyncConfig` by overriding a new method:
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
I particularly prefer this option as you can use an `AsyncUncaughtExceptionHandler` to implement a global exception-handling strategy for your application, such as logging the exception or sending an email notification.

# Conclusion
In this blog post, we've discussed how to use the Spring `@Async` annotation to execute methods asynchronously and how to use and configure a thread executor bean to manage the threads used by async methods.  
We also covered how to handle exceptions and receive returned values from asynchronous methods. Applying this tips we can improve the performance and responsiveness of our application and avoid blocking the main thread while long-running tasks are being executed.

Happy code!