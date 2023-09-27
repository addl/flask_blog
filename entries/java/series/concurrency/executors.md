## poster
![Java Executor Framework](https://drive.google.com/uc?export=view&id=1MXJoAF9EszVJPkh868HVbKwN21ntPrHu)

## Introduction
So far, in this [Java Concurrent](http://myrefactor.com/en/serie/1/posts) serie we have covered two ways of creating threads:

1. A class that implements the `Runnable` interface: This is the code you want to implement in a concurrent way. 
2. An instance of the `Thread` class: This is the thread that is going to execute the code in parallel. 

The drawbacks of these approaches is that your responsable for the creation and managing the threads, managing threads can be complex and error-prone. 
To address this, Java provides the Executor Framework, a high-level abstraction that simplifies thread management. 
In this article, we will explore the characteristics of the Executor Framework, its components, and how to use them effectively.

## Characteristics of the Executor Framework
* You don't need to create any Thread objects. If you want to execute a concurrent task, you only need an instance of class that implements the Runnable interface and send it to the executor. It will allocate the thread that will execute the task. 
* Executors reduce the overhead introduced by thread creation reusing the threads. Internally, it manages a pool of threads named worker-threads. If you send a task to the executor and a worker-thread is idle, the executor uses that thread to execute the task. 
* It's easy to control the resources used by the executor. You can limit the maximum number of worker-threads of your executor. If you send more tasks than worker-threads, the executor stores them in a queue. When a worker-thread finishes the execution of a task, they take another from the queue. 
* You have to finish the execution of an executor explicitly. You have to indicate to the executor that it has to finish its execution and kill the created threads. If you don't do this, it won't finish its execution and your application won't end. 


## Main Components of the Executor Framework

1. `Executor` Interface: The Executor interface lies at the heart of the Executor Framework. It defines a single method, **execute(Runnable task)**, which takes a Runnable object and executes it asynchronously in a separate thread. This interface serves as a foundation for other components of the framework. 
2. `ExecutorService` Interface: The ExecutorService interface extends the Executor interface and provides additional methods to manage and control the execution of tasks. It represents an asynchronous execution service that manages a pool of threads. Some important methods include **submit()**, **invokeAll()**, **invokeAny()**, and **shutdown()**. ExecutorService implementations provide advanced features like task scheduling, result retrieval, and thread pooling. 
3. `ThreadPoolExecutor` Class: is one of the most commonly used implementations of the `ExecutorService` interface. It manages a fixed-size thread pool and reuses threads, thus avoiding the overhead of thread creation for each task. It provides various configurable parameters to control the pool size, task queueing, and thread timeout. 
4. `Executors` Class: The Executors class provides several factory methods to create pre-configured instances of ExecutorService. These methods simplify the process of creating thread pools with different characteristics, such as fixed-size, cached, or scheduled. 

> It's important to note that not all algorithms are inherently suitable for multi-threading. The effectiveness of parallelization depends on the nature of the algorithm, the size of the problem, and the available hardware resources. Additionally, parallelizing algorithms requires careful consideration of data dependencies, synchronization, and load balancing to ensure correct and efficient execution.

## Case of study. Matrix multiplication
Let's illustrate the usage of the `Executor Framework` with a simple example. We start from a serial, non-parallel variant of Matrix multiplication.

> To multiply two matrices, the number of columns in matrix A is equal to the number of rows in matrix B and viceversa.

Consider two matrices: Matrix A with dimensions (m x n) and Matrix B with dimensions (n x p). The resulting matrix C will have dimensions (m x p).

To compute the elements of matrix C, the following steps are performed:

1. For each element in the resulting matrix C, locate the corresponding row and column in the input matrices A and B. 
2. Take the [dot product](https://www.mathsisfun.com/algebra/vectors-dot-product.html) of the elements in the selected row of matrix A and the selected column of matrix B. 
3. Sum the products obtained in step 2 to calculate the value of the corresponding element in matrix C. 
4. Repeat steps 1-3 for all elements in matrix C to compute the entire matrix. 

Mathematically, the calculation for each element `C[i][j]` in the resulting matrix C can be expressed as follows:

`C[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + ... + A[i][n-1] * B[n-1][j]`

## Serial version of Matrix multiplication
Here is the implementation of a non-parallel matrices multiplication algorithm:
```java
public class MatrixMultiplicationSimple {

	public static void main(String[] args) {
		int[][] matrixA = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };

		int[][] matrixB = { { 10, 11, 12 }, { 13, 14, 15 }, { 16, 17, 18 } };
		
		int[][] result = multiplyMatrices(matrixA, matrixB);

		// Print the result matrix
		System.out.println("Result:");
		for (int i = 0; i < result.length; i++) {
			for (int j = 0; j < result[0].length; j++) {
				System.out.print(result[i][j] + " ");
			}
			System.out.println();
		}
	}

	public static int[][] multiplyMatrices(int[][] matrixA, int[][] matrixB) {
		int rowsA = matrixA.length;
		int colsA = matrixA[0].length;
		int colsB = matrixB[0].length;

		int[][] result = new int[rowsA][colsB];

		for (int i = 0; i < rowsA; i++) {
			for (int j = 0; j < colsB; j++) {
				int sum = 0;
				for (int k = 0; k < colsA; k++) {
					sum += matrixA[i][k] * matrixB[k][j];
				}
				result[i][j] = sum;
			}
		}
		return result;
	}

}

```

## Parallel version of Matrix multiplication
In order to implement a multithreading version. Let's define in the first place our task by implementing the `Runnable` interface:

```java
class MatrixMultiplicationTask implements Runnable {
    private final int[][] matrixA;
    private final int[][] matrixB;
    private final int[][] result;
    private final int row;
    private final int col;

    public MatrixMultiplicationTask(int[][] matrixA, int[][] matrixB, int[][] result, int row, int col) {
        this.matrixA = matrixA;
        this.matrixB = matrixB;
        this.result = result;
        this.row = row;
        this.col = col;
    }

    @Override
    public void run() {
        int sum = 0;
        for (int k = 0; k < matrixA[row].length; k++) {
            sum += matrixA[row][k] * matrixB[k][col];
        }
        result[row][col] = sum;
    }
}
```
As you can see, this task computes one element in the resulting matrix, the element in `result[row][col]`.
We will multiply the matrices using `ExecutorService` and its method **execute** passing an instance of the task `MatrixMultiplicationTask`.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MatrixMultiplicationParallel {

	public static void main(String[] args) {
		int[][] matrixA = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };

		int[][] matrixB = { { 10, 11, 12 }, { 13, 14, 15 }, { 16, 17, 18 } };

		int[][] result = new int[matrixA.length][matrixB[0].length];
		int numThreads = matrixA.length * matrixB[0].length;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);

		for (int i = 0; i < matrixA.length; i++) {
			for (int j = 0; j < matrixB[0].length; j++) {
				executor.execute(new MatrixMultiplicationTask(matrixA, matrixB, result, i, j));
			}
		}

		executor.shutdown();

		// Wait for all tasks to complete
		while (!executor.isTerminated()) {
			// Do nothing and wait
		}

		// Print the result matrix
		System.out.println("Result:");
		for (int i = 0; i < result.length; i++) {
			for (int j = 0; j < result[0].length; j++) {
				System.out.print(result[i][j] + " ");
			}
			System.out.println();
		}
	}

}
```

In the above code we basically did:
1. Define the matrices that we will multiply.
2. Calculate the total number of threads required for the multiplication (which is the number of elements in the result matrix), and create a fixed thread pool with that size using **Executors.newFixedThreadPool(numThreads)**. 
3. Iterate over each element in the result matrix and submit a `MatrixMultiplicationTask` to the executor for execution. 
4. Submitting all the tasks, we call **executor.shutdown()** to initiate the graceful shutdown of the executor. 
5. Finally, we wait for all tasks to complete by checking **executor.isTerminated()**, and print the resulting matrix. 


## Conclusion
The Executor Framework in Java provides a high-level abstraction for managing threads and simplifies the process of creating concurrent applications. Its key components, such as the Executor and ExecutorService interfaces, along with ThreadPoolExecutor and Executors class, allow developers to efficiently manage thread execution. By utilizing the Executor Framework, developers can harness the power of multithreading while avoiding the complexities associated with manual thread management.

## References

[How to Multiply Matrices](https://www.mathsisfun.com/algebra/matrix-multiplying.html)