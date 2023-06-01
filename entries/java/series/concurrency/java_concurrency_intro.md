## poster
![Object Usage over time in JVMs](https://drive.google.com/uc?id=1Dj534IlTJhUDy6wAQGGFB9xuRcrSNVmA)

## Introduction
Multithreading is a fundamental concept in Java programming that allows the execution, concurrently, of multiple threads.
For a concurrent application, we have to create different execution threads that runs in parallel. In Java there are two basic ways of creating execution threads, the first one is by extending the Thread class and the second by implementing the Runnable interface.

In this article, we will dive into the Thread class and explore its properties and methods for creating and running threads in Java.

## Background
The first thing we should be aware of, is that all Java programs have at least one `Thread`, it is called the `main` Thread, and starts executing when we invoke the `main` method of the root class in our application:
````java
public class MyApplication {
	public static void main(String[] args) {
		// our code
	}
}
````
This is the only thread in **non-concurrent** applications and the first one in **concurrent applications**.


## The Thread class
The Thread class in Java represents a thread of execution. It provides essential functionalities and operations to control and manage threads.
In order to create a thread we just need to extend the Thread class and implement its `run` method:
````java
public class MyThread extends Thread {
    public void run() {
        // Code to be executed in the thread
    }
}
````


## A custom thread in action
For demonstrating how threads works let's create a simple application with one custom thread.
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
In the code above:
1. We crate a class `MyThread` that extends the class `Thread` and we implement the **run** method. 
2. We get the instance of the thread by using **currentThread()**. This method is a static method of the Thread class that returns an instance of the current `Thread`. 
3. Then we print a message to identify our Thread with its unique ID, we get the ID by calling **getId()** method of `Thread` class.

Now we will need a main thread to execute our application:
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
Above we did the following:
1. In the first line `mainThread` variable holds a reference to the currently executing thread, which is the **main thread of the program**. 
2. The next line, creates an instance of the `MyThread` class. This creates a new thread object but **does not start its execution yet**.
3. In order to create a new execution thread we call **start()** method from a thread instance: `myThread.start();`.

By executing the program, we get something similar to this:
````commandline
The Main Thread with ID: 1
My thread with ID: 23
````

You will notice how the second line takes a bit(1000ms = 1sec) to show in the console. Also notice how the main thread it is not interrupted by calling the **start** method of `myThread` and continues to its print statement, without waiting for `myThread`'s execution.
> In Java, thread IDs are system-dependent, and their values are not guaranteed to be consecutive. 

Now that we see in action how to create threads let's delve into more details.


## Types of thread
In Java, threads can be classified into two types based on their behavior and their impact on **the termination of the program**: `daemon` threads and `non-daemon` threads.

### Daemon Threads: 
* Run in the background to perform tasks that **don't necessarily need to complete** before the program terminates. 
* The JVM **will not wait** for any daemon threads to complete before terminating the program. 
* Are typically used for tasks such as garbage collection, monitoring, or other maintenance activities that can run independently in the background without affecting the main functionality of the program. 


### Non daemon threads:
* Are user threads that are explicitly created by the program and perform tasks that are critical to the program's functionality. 
* The JVM **waits for all non-daemon threads** to complete their execution before terminating the program. 
* Are essential for the execution of the program's main logic and **should complete their tasks** before the program terminates.

In summary, the distinction between daemon and non-daemon threads in Java is primarily related to the JVM's behavior when terminating the program. 
To notice the difference, let's make our custom thread a daemon:
````java
public static void main(String[] args) {
    Thread mainThread = Thread.currentThread();
    MyThread myThread = new MyThread();
    myThread.setDaemon(true);
    myThread.start();
    System.out.println("The Main Thread with ID: " + mainThread.getId());
  }
````
Now the output is:
````commandline
The Main Thread with ID: 1
````
Notice how the JVM terminates the main thread **without** waiting for the termination of our custom thread.
> We must set the daemon as true before calling **start** method.

## Thread priority
All threads in Java have priority, it is an integer value from 0 (Thread.MIN_PRIORITY) to 10 (Thread.MAX_PRIORITY). By default, a thread is created with priority 5 (Thread.NORM_PRIORITY).

The priority is a hint to the JVM and the operating system about which threads are `preferrable`, but there is no guarantee of the order of execution.

## Thread status
A thread can have several states throughout its lifecycle:

1. New: The thread is in the new state when it is created but not yet started. It has not yet begun its execution. 
2. Runnable: In the runnable state, the thread is eligible to run, and the underlying operating system scheduler will assign it CPU time whenever possible. 
3. Blocked/Waiting: A thread can enter a blocked or waiting state when it is waiting for a lock or waiting for a specific condition to be satisfied before it can proceed. 
4. Timed Waiting: Similar to the blocked/waiting state, nut he has time limit. 
5. Terminated: The thread reaches the terminated state when its execution has completed, either by finishing its run() method or being explicitly terminated.

## Methods in Thread class
The `Thread` class has a lot of methods allowing developers to get and set information:

1. **start()**: Initiates the execution of the thread and invokes the operating system to allocate resources for the thread.  
2. **run()**: Contains the code that will be executed by the thread. 
3. **getId()**: Returns the unique identifier assigned to the thread. 
4. **getName()** and **setName(String name)**: getName() retrieves the name of the thread, while setName(String name) sets a new name for the thread. 
5. **sleep(long millis)**: Pauses the execution of the current thread for the specified number of milliseconds. 
6. **join()**: Waits for the thread on which it is called to complete its execution. 
7. **interrupt()**: Interrupts the execution of a thread by setting its interrupt status. It is a cooperative mechanism for signaling a thread to stop execution gracefully. 
8. **isInterrupted()**: Checks if the current thread has been interrupted. 
9. **yield()**: Suggests that the currently executing thread voluntarily gives up the CPU to allow other threads to run. It is a hint to the scheduler to switch execution to another thread. 
10. **getPriority()** and **setPriority(int priority)**: Get or set the priority of the thread. 
11. **isAlive()**: Checks if the thread is currently executing or has terminated. It returns a boolean value indicating the thread's status. 

## Conclusions
The Thread class is a crucial component in Java concurrency and multithreading. It provides the basic functionalities to create, start, and manage threads in Java to some extent.
In this article we have described the Thread class and create a simple application in order to understand how concurrency works in multithreading execution context.
In the next post of this series, we will implement a classic Producer and Consumer problem using the knowledge we have covered here.

