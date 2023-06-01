## poster
![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1Y3RF8GlqW6qn_S3C8fFjZvoNHmnPE1pR)

## Introduction
JMH (Java Microbenchmark Harness) is a powerful benchmarking tool used to measure the performance of Java code. 
It provides a reliable and standardized approach to benchmarking, allowing developers to accurately assess the performance characteristics of their code. In this blog, we will explore the features and usage of JMH, along with best practices for benchmarking Java applications.

## Why Use JMH
JMH offers several advantages for benchmarking Java code:

* Standardized Benchmarking: JMH provides a standardized framework for benchmarking Java code, ensuring consistent and reliable results across different environments. 
* Precise Measurement: JMH takes care of various factors that can affect benchmarking results, such as JVM warm-up, Just-In-Time (JIT) compilation, and thread synchronization. This ensures accurate measurement of code performance. 
* Benchmark Modes: JMH supports different benchmark modes, including throughput, average time, and sample time. These modes allow you to focus on specific performance aspects based on your requirements. 
* Parameterization: JMH supports parameterization of benchmarks, allowing you to test your code with different input scenarios. This helps identify performance variations and optimize your code accordingly. 
* Integration with Profilers: JMH seamlessly integrates with profilers and diagnostic tools like Java Flight Recorder (JFR) and JMH-profiler. This enables in-depth analysis of benchmark results to identify performance bottlenecks and optimize code. 

Before we go deep into JMH benchmark coding, we have to understand its key elements.

## The Benchmark annotation
Use the `@Benchmark` annotation provided by JMH  to mark the methods you want to benchmark. JMH will execute these methods and measure their performance.
```java
@Benchmark
public void myRoutineToComputeSomething() {
    // Code to be benchmarked
}
```

## Benchmark Types
There are four different benchmark types available:

1. Mode.AverageTime: Measures the average time taken for each operation. 
2. Mode.SampleTime: Time for each operation, including min and max. 
3. Mode.SingleShotTime: Time for a single operation. 
4. Mode.Throughput: Measures the number of operations per unit of time. 
5. Mode.All: All of the above. 

We can set the desired modes with the annotation `@BenchmarkMode(...)`. The default mode is `Mode.Throughput`.

## Controlling Warm-up and Measurement
Warm-up iterations allow the JVM to reach a stable state before measurements start. Measurement iterations are used to collect the benchmark data.
You can configure the number of warm-up and measurement iterations using the `@Warmup` and `@Measurement` annotations, for instance:

```java
@Benchmark
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public void myRoutineToComputeSomething() {
    // Code to be benchmarked
}
```
The above configuration runs three warm-up iterations followed by five measurement iterations.

## Benchmarks' setup and state
The state class marked with `@State` can contain fields representing the state variables required for the benchmark and/or  initial state by using `@Setup` methods within the state class. For example:
```java
@State(Scope.Benchmark)
public class MyBenchmarkState {
    private int myParameter;

    @Setup
    public void setup() {
        // Initialize the state variables
        myParameter = 42;
    }
}

```
The **setup()** method will be called once before each benchmark iteration to set up the initial state.

## Parameterized Benchmarks
JMH supports parameterization of benchmarks to test code with different input values. 
This can be achieved using the `@Param` annotations:

```java
@State(Scope.Benchmark)
public static class BenchmarkState {
    @Param({"10"})
    public int number;
}
```

The value of `number` variable is specified in `@Param` annotation.


## Creating the maven project
The easiest way to execute JMH benchmarks is to create a maven project using the archetypes of JMH, we can generate the project from command line or using any IDE.

### Using the command line
To generate the maven project from command line, execute the command:

```commandline
$ mvn archetype:generate -DinteractiveMode=false -DarchetypeGroupId=org.openjdk.jmh \
    -DarchetypeArtifactId=jmh-java-benchmark-archetype -DgroupId=com.myrefactor \
    -DartifactId=benchmarking -Dversion=1.0
```

### Using Eclipse IDE
Simply create a new maven project from File -> New -> Maven Project menu and make sure to enter the archetype as follows:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1Y2QuEM7Ek7WByxWLQqAg6PB9sIQJ_XXx)


In both cases you will end up with a project and a main class called `MyBenchmark`, with the following content:
```java
public class MyBenchmark {

    @Benchmark
    public void testMethod() {
        // This is a demo/sample template for building your JMH benchmarks. Edit as needed.
        // Put your benchmark code here.
    }
    
}
```
We will modify this class and will create a benchmark to a Fibonacci serie algorithm.

## Writing our benchmark
```java
public class MyBenchmark {
	
    @State(Scope.Benchmark)
    public static class BenchmarkState {
        @Param({"10"})
        public int number;
    }

    @Benchmark
    @Warmup(iterations = 3)
    @Measurement(iterations = 5)
    public void testMethod(BenchmarkState state) {
    	int number = state.number;
    	computeFibonacciLoop(number);
    }
    
    public long computeFibonacciLoop(int number) {
    	if (number <= 1) {
			return number;
		}
		int prev = 0;
		int curr = 1;
		for (int i = 2; i <= number; i++) {
			int temp = curr;
			curr = prev + curr;
			prev = temp;
		}
		return curr;
	}
    
    public static void main(String[] args) throws RunnerException {
        Options options = new OptionsBuilder()
            .include(MyBenchmark.class.getSimpleName())
            .forks(1)
            .build();
        new Runner(options).run();
    }

}
```
The above code wrap the execution of the **computeFibonacciLoop** method inside another method **testMethod**. This is useful to isolate the  method we want to benchmark from the benchmark scope and setup.

## Executing the benchmarks
Once your benchmark code is ready to execute. You have to build it with the following command:
```commandline
$ mvn clean verify
```

After the build is done, you will get the self-contained executable JAR, which holds your benchmark, and all essential JMH infrastructure code:
```commandline
java -jar target/benchmarks.jar
```
> Notice how the generated `jar` file is called `benchmarks.jar`, this is a result of the archetype maven project.

The output will be:
```commandline
# Run progress: 80,00% complete, ETA 00:01:20
# Fork: 5 of 5
# Warmup Iteration   1: 2139626278,115 ops/s
# Warmup Iteration   2: 2035475517,010 ops/s
# Warmup Iteration   3: 2020375919,007 ops/s
Iteration   1: 2023195836,546 ops/s
Iteration   2: 2026736738,867 ops/s
Iteration   3: 2090416921,603 ops/s
Iteration   4: 2062121040,459 ops/s
Iteration   5: 2012130960,572 ops/s


Result "com.myrefactor.benchmarking.MyBenchmark.testMethod":
  1915365597,778 ?(99.9%) 89718491,176 ops/s [Average]
  (min, avg, max) = (1473967335,788, 1915365597,778, 2090416921,603), stdev = 119771618,852
  CI (99.9%): [1825647106,602, 2005084088,954] (assumes normal distribution)


# Run complete. Total time: 00:06:41

REMEMBER: The numbers below are just data. To gain reusable insights, you need to follow up on
why the numbers are the way they are. Use profilers (see -prof, -lprof), design factorial
experiments, perform baseline and negative tests that provide experimental control, make sure
the benchmarking environment is safe on JVM/OS/HW level, ask for reviews from the domain experts.
Do not assume the numbers tell you what you want them to tell.

Benchmark               (number)   Mode  Cnt           Score          Error  Units
MyBenchmark.testMethod        10  thrpt   25  1915365597,778 ? 89718491,176  ops/s
```

## Results
Interpreting JMH benchmark results requires the understanding of several metrics:

* Throughput: Represents the number of operations executed per unit of time. Higher throughput values indicate better performance. 
* Average Time: Represents the average time taken for each operation. Lower average time values indicate better performance. 
* Percentiles: Provides information about the distribution of timings. For example, the 99th percentile indicates the time below which 99% of the measured values fall. Percentiles help identify outliers and potential performance issues. 


### Interpreting Results
These metrics must be analyzed in order to identify performance bottlenecks and areas for optimization. In our example output: 

1. The benchmark achieved a throughput of approximately 1,915,365,597.778 operations per second, with an error margin of 89,718,491.176 ops/s. The "? (99.9%)" indicates that this is the confidence interval. 
2. The minimum, average, and maximum scores observed during the benchmark runs were 1,473,967,335.788 ops/s, 1,915,365,597.778 ops/s, and 2,090,416,921.603 ops/s, respectively. 
3. The standard deviation (stdev) of the scores is 119,771,618.852 ops/s. A higher standard deviation suggests that the benchmark scores have a larger degree of variability or dispersion. 


## Best Practices and Tips
Here are some best practices and tips for effective benchmarking with JMH:

* Warm-up Strategies: Design proper warm-up strategies to allow the JVM to reach an optimized state before measurements start. This ensures stable and accurate benchmark results. 
* JVM Options: Configure JVM options, such as heap size and garbage collector settings, to ensure optimal performance during benchmarking. 
* Avoid Common Pitfalls: Be aware of common pitfalls in benchmarking, such as dead code elimination and method inlining by the JIT compiler. Use JMH-specific annotations like `@CompilerControl` or `@BenchmarkMode(Mode.SingleShotTime)` to mitigate these issues. 
* Benchmark Single Methods: Benchmark individual methods rather than entire components or systems. This provides focused results and allows for targeted optimization. 
* Validate and Verify Results: Validate benchmark results by running multiple iterations and verifying consistency. Ensure that any performance improvements are statistically significant. 

## Trouble shooting
### Not using the archetype
I receive the following error when trying to set up a project from Eclipse without using the archetype and specifying the dependencies manually in the `pom.xml`.
```commandline
ERROR: Unable to find the resource: /META-INF/BenchmarkList
```
It is recommended to generate the project using the archetype.

### Annotation processing
JMH finds your benchmarks methods annotated with `@Benchmark`, you have to enable annotation processing in your IDE, otherwise you will face the following error:

```commandline
No benchmarks found, skipping.
```


## Conclusion
In this blog post, we explored the features and usage of JMH (Java Microbenchmark Harness) for benchmarking Java code. We discussed the importance of using JMH for accurate performance measurement, and we covered topics such as setting up JMH, writing benchmarks using a Fibonacci algorithm, controlling warm-up and measurement, parameterized benchmarks using its state and interpreting results. Finally we covered some of the best practices for effective benchmarking.

## References

[JMH Official Website](https://github.com/openjdk/jmh)

[Microbenchmarks With JMH](https://blog.avenuecode.com/java-microbenchmarks-with-jmh-part-1)

[Architect Benchmarking](https://www.oracle.com/technical-resources/articles/java/architect-benchmarking.html)