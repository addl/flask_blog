## Introduction
In this article, you will learn the fundamental concepts of Garbage Collection in Java. 
I will explain what is garbage collection and its importance for the health of Java applications. 
We also describe the different processes like object marking and the different generations in which the heap is divided.
Finally, the post explains the kinds of garbage collectors and tools to monitor the heap and activity of running Java applications.

## What is garbage collection
In a programming language like C, allocating and deallocating memory is a manual process. 
In Java, process of deallocating memory is handled automatically by the garbage collector. 

Automatic garbage collection is the process of looking at heap memory, identifying which objects are being used and which are not, and proceeding with the deletion of unused objects. 
An in-use object, or a referenced object, means that some part of your program still maintains a pointer to that object. 
On the other hand, an unused object, or unreferenced object, is no longer referenced by the code of your program. 
So the memory used by an unreferenced object can be reclaimed.
In a nutshell, garbage collection is a process to free-up memory.

## garbage collection's relevance
Garbage collection in Java, frees the programmer from manually dealing with memory deallocation. 
As a result, certain categories of application program bugs are eliminated or substantially reduced by GC:

* Dangling pointer bugs, which occur when a piece of memory is freed while there are still pointers to it, and one of those pointers is dereferenced. By then the memory may have been reassigned to another use with unpredictable results.
* Double free bugs, which occur when the program tries to free a region of memory that has already been freed and perhaps already been allocated again.
* Certain kinds of memory leaks, in which a program fails to free memory occupied by objects that have become unreachable, which can lead to memory exhaustion.

## Marking process
The first step in the garbage collection is called marking. 
This is where the garbage collector identifies which pieces of memory are in use and which are not.

![Garbage Collector Marking Process](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/gcslides/Slide3.png)

Referenced objects are shown in blue. Unreferenced objects are shown in gold. 
All objects are scanned in the marking phase to make this determination. 
This process of 'marking' can be very time-consuming and become inefficient as objects in a system keep growing and growing.

## Object generation classification
Empirical analysis of applications has shown that most objects are short-lived, take a look at the following chart:

![Object Usage over time in JVMs](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/ObjectLifetime.gif)

As you can see, fewer objects remain referenced over time. In fact, most objects have a very short life as shown by the higher values on the left side of the graph.

The above information has been used to enhance the JVM Garbage Collection process, thus, the heap memory has been split out into several areas, as shown in the below picture:  

![Heap Generations](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/gcslides/Slide5.png)

### The Young Generation
All new objects are allocated and aged in the young generation area. When this area fills up, a `minor garbage collection` is executed. 
Minor collections can be optimized assuming a high object mortality rate. A young generation full of dead objects is collected very quickly.
Some surviving objects are aged and eventually move to the old generation.


### The Old Generation
This zone is used to store long surviving objects. 
Typically, a threshold is set for young generation object and when that age is met, the object gets moved to the old generation. 
Eventually the old generation needs to be collected. This event is called a `major garbage collection`.

Often a major collection is much slower because it involves all live objects. 
So for Responsive applications, major garbage collections should be minimized.


### The Permanent generation
Finally, the permanent generation contains metadata required by the JVM to describe the classes and methods used in the application. 
The permanent generation is populated by the JVM at runtime based on classes in use by the application. 
In addition, Java SE library classes and methods may be stored here.

Classes may get collected (unloaded) if the JVM finds they are no longer needed and space may be needed for other classes. 
The permanent generation is included in a `full garbage collection`.

> In order to perform a garbage collection, being minor, major or full, the JVM must stop the application from running for at least a short time. This process is called **stop-the-world**.
> This means all the threads, except for the GC threads, will stop executing until the GC threads are executed and objects are freed up by the garbage collector.


## Monitoring Heap
Now that we have the know-how about the different areas of the JVM's heap, we can inspect it on our own. I will use VisualVM, a visual tool that provides lightweight profiling capabilities for the JVM. 
There are plenty of other mainstream profiling tools. 
However, VisualVM is free and comes bundled with the JDK 6U7 release until early updates of JDK 8. 
For other versions of Java, like 1.9+, Java VisualVM is available as a [standalone application](https://visualvm.github.io/).

In my case I have installed Java 1.8, so I have VisualVM in my JDK installation's bin directory:`C:\Program Files\Java\jdk-11.0.12\bin`, the file is: `jvisualvm.exe`, so by just double-clicking it I got the tool up and running.

![Visual VM tool](https://drive.google.com/uc?id=1G_eD8tNn2RHbRup-Zbqa-UEI_ZCrx7_u)

As you can see it lists all Java applications running currently, for instance I have opened PyCharm and Eclipse.
We are looking to inspect the heap memory, to do that we need to install a plugin called `VisalGC`. 
So let's click in the menu: **Tools** --> **Plugins**, then open the tab **Available Plugins** and install it, below more details:

![Heap Generations](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/visualvm/VisualGCIns02.png)

After completing the wizard, we should receive successful message meaning installation is completed.

### Analyze an application
Now let's analyze my Eclipse instance, from the home page of VisualVM, I will right-click the Eclipse application in the Local applications list of the Applications tab and then select **Open**.
Notice a number of tabs are loaded on the right side of the interface. I will go to **Visual GC** tab, and I can see the following interface:

![Visual VM tool](https://drive.google.com/uc?id=1UJxRsEImGCoaUuds_2PethVXjXdCUyrj)

If I perform a task in Eclipse, for example performing a string search in my workspace, I notice rapidly how it impacts the charts and metrics.
Feel free to try the other tabs and see what information is presented about the JVM.

## Ways of performing Garbage Collection

The traditional Oracle HotSpot JVM has four ways of performing the GC activity:

### Serial GC
The serial collector is the default for client style machines, where just one thread executed the GC.
With the serial collector, both minor and major garbage collections are done serially (using a single virtual CPU). Hence, its name.

Serial GC uses a **mark-compact** collection method. 
This method moves older memory to the beginning of the heap so that new memory allocations are made into a single continuous chunk of memory at the end of the heap. 
This compacting of memory makes it faster to allocate new chunks of memory to the heap.

To enable the Serial Collector use `-XX:+UseSerialGC`, for instance:
````commandline
java -XX:+UseSerialGC -jar c:\javademos\demo\jfc\Java2D\Java2demo.jar
````
A common use for the Serial GC is in environments where a high number of JVMs are run on the same machine (in some cases, more JVMs than available processors!).
In such environments when a JVM does a garbage collection it is better to use only one processor to minimize the interference on the remaining JVMs, even if the garbage collection might last longer.

### Parallel GC
The parallel garbage collector uses multiple threads to perform the young generation garbage collection.
By default, on a host with N CPUs, the parallel garbage collector uses N garbage collector threads in the collection. 
The number of garbage collector threads can be controlled with command-line options: `-XX:ParallelGCThreads=<desired number>`

The Parallel collector is also called a throughput collector. Since it can use multiple CPUs to speed up application throughput.
Basically we can run parallel garbage collector in two modes:  

1. A multi-thread young generation collector with a single-threaded old generation collector: `-XX:+UseParallelGC`.
2. Both a multithreading young generation collector and multithreading old generation collector: `-XX:+UseParallelOldGC`.

### Concurrent Mark Sweep (CMS)
Similar to parallel, also allows the execution of some application threads and reduces the frequency of stop-the-world GC.
It attempts to minimize the pauses due to garbage collection by doing most of the garbage collection work concurrently with the application threads. 
Normally the concurrent low pause collector does not copy or compact the live objects. 
A garbage collection is done without moving the live objects. If fragmentation becomes a problem, allocate a larger heap.

> CMS collector on young generation uses the same algorithm as that of the parallel collector.

The CMS collector should be used for applications that require low pause times and can share resources with the garbage collector. 
Examples include desktop UI application that respond to events, a webserver responding to a request or a database responding to queries.

To enable the CMS Collector use: `-XX:+UseConcMarkSweepGC` and to set the number of threads use: `-XX:ParallelCMSThreads=<n>`.

### G1 
G1 runs in parallel and concurrently like CMS, but functions differently than CMS, and is designed to be the long term replacement for the CMS collector.
The G1 collector is a parallel, concurrent, and incrementally compacting low-pause garbage collector that has quite a different layout from the other garbage collectors described in this post.
In subsequent entries, I will describe in detail how it works.

To enable the G1 Collector use: `-XX:+UseG1GC`

Interestingly, taking a look at my Eclipse's instance from VisualVM, it runs using G1:
````commandline
-Dosgi.requiredJavaVersion=11
-Dosgi.instance.area.default=@user.home/eclipse-workspace
-XX:+UseG1GC
````

> Modern JVMs like Azul Zing use Continuously Concurrent Compacting Collector (C4), which eliminates the stop-the-world GC pauses, thus increasing the scalability.

## Conclusion
In this entry, we have learned the fundamentals of Java Garbage Collection by introducing the different areas of the memory heap, the importance of garbage collection running automatically. 
We also covered the marking process and the generation classification. We have seen an important tool to monitoring running Java applications.
Finally, we learned the different ways in which GC runs.


## reference

[https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/index.html](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/index.html)

[https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/sizing.html#heap_parameters](https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/sizing.html#heap_parameters)

[https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/collectors.html](https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/collectors.html)
