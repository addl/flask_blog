## poster
![Java Executor Framework](https://drive.google.com/uc?export=view&id=1MXJoAF9EszVJPkh868HVbKwN21ntPrHu)

## Introducción
Hasta ahora, en esta serie [Java Concurrent](http://myrefactor.com/en/serie/1/posts) hemos aprendido dos formas de crear hilos:

1. Una clase que implementa la interfaz `Runnable`: con el código que deseamos implementar de manera concurrente. 
2. Una instancia de la clase `Thread`: siendo el hilo que va a ejecutar el código en paralelo. 


Los inconvenientes de estos enfoques es que somos responsables de la creación y gestión de los hilos, la gestión de subprocesos puede ser compleja en algunas circunstancias y, por tanto, propensa a errores.
Para mitigar esto, Java proporciona the `Executor Framework`, una abstracción de alto nivel que simplifica la gestión de subprocesos.
En este artículo, exploraremos las características del Executor Framework, sus componentes y cómo usarlos de manera efectiva.
> A lo largo de este post, los términos "hilo" y "subproceso" son usados indiferentemente.

## Características del Framework Ejecutor
* No necesita crear ningún objeto Thread. Si desea ejecutar una tarea concurrente, solo necesita una instancia de clase que implemente la interfaz Runnable y envíela al ejecutor. Asignará el hilo que ejecutará la tarea. 
* Los ejecutores reducen la sobrecarga introducida por la creación de hilos reutilizándolos. Internamente, administra un conjunto de subprocesos denominados subprocesos de trabajo. Si envía una tarea al ejecutor y un subproceso de trabajo está inactivo, el ejecutor usa ese subproceso para ejecutar la tarea. 
* Es fácil controlar los recursos utilizados por el ejecutor. Puede limitar el número máximo de hilos de trabajo. Si envía más tareas que subprocesos de trabajo, el ejecutor los almacena en una cola. Cuando un subproceso de trabajo finaliza la ejecución de una tarea, toma otra de la cola. 
* Tienes que terminar la ejecución de un ejecutor explícitamente. Tienes que indicarle al ejecutor que tiene que terminar su ejecución y matar los hilos creados. 

## Componentes principales del Ejecutor Framework

1. La interfaz `Executor`: La interfaz Executor es el corazón del Executor Framework. Define un único método, **execute(Runnable task)**, que toma un objeto Runnable y lo ejecuta de forma asíncrona en un subproceso. Esta interfaz sirve como base para los otros componentes del marco. 
2. La interfaz `ExecutorService`: La interfaz ExecutorService extiende la interfaz Executor y proporciona métodos adicionales para administrar y controlar la ejecución de tareas. Representa un servicio de ejecución asincrónica que administra un conjunto de subprocesos. Algunos métodos importantes incluyen **submit()**, **invokeAll()**, **invokeAny()** y **shutdown()**. 
3. La clase `ThreadPoolExecutor`: es una de las implementaciones más utilizadas de la interfaz `ExecutorService`. Administra un grupo de subprocesos de tamaño fijo y reutiliza los subprocesos, evitando así la sobrecarga de la creación de subprocesos para cada tarea. Proporciona varios parámetros configurables para controlar el tamaño del grupo(pool), la cola de tareas y el tiempo de espera del subproceso. 
4. La clase `Executors`: La clase Executors proporciona varios métodos para crear instancias pre-configuradas de ExecutorService. Estos métodos simplifican el proceso de creación de grupos de subprocesos con diferentes características, como el tamaño o la caché. 

> Es importante tener en cuenta que no todos los algoritmos son adecuados para múltiples hilos. La efectividad de la paralelización depende de la naturaleza del algoritmo, el tamaño del problema y los recursos de hardware disponibles. Además, la paralelización de algoritmos requiere una cuidadosa consideración de las dependencias de datos, la sincronización y el balance de carga para garantizar una ejecución correcta y eficiente. 

## Caso de estudio. Multiplicación de matrices
Ilustremos el uso del `Executor Framework` con un ejemplo simple. Partimos de una variante serial, no paralela de la multiplicación de matrices.

> Para multiplicar dos matrices, el número de columnas de la matriz A debe ser igual al número de filas de la matriz B y viceversa.

Considere dos matrices: Matriz `A` con dimensiones `(m x n)` y Matriz `B` con dimensiones `(n x p)`. La matriz `C` resultante tendrá dimensiones `(m x p)`.

Para calcular los elementos de la matriz C, se realizan los siguientes pasos:

1. Para cada elemento de la matriz C resultante, busque la fila y la columna correspondientes en las matrices de entrada A y B. 
2. Tome el [dot product](https://www.mathsisfun.com/algebra/vectors-dot-product.html) de los elementos en la fila seleccionada de la matriz A y la columna seleccionada de la matriz B. 
3. Sume los productos obtenidos en el paso 2 para calcular el valor del elemento correspondiente en la matriz C. 
4. Repita los pasos 1-3 para todos los elementos de la matriz C para calcular la matriz completa. 

Matemáticamente, el cálculo de cada elemento `C[i][j]` en la matriz C resultante se puede expresar de la siguiente manera:

`C[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + ... + A[i][n-1] * B[n-1][j]`

## Versión en serie de la multiplicación de matrices
Aquí está la implementación de un algoritmo de multiplicación de matrices sin usar hilos, solo el hilo principal(main):

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

## Versión paralela de la multiplicación de matrices
Con el fin de implementar una versión multihilo. Definamos en primer lugar nuestra tarea implementando la interfaz `Runnable`:

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
Como puede ver, esta tarea calcula un elemento en la matriz resultante, el elemento en `resultado[fila][columna]`.
Multiplicaremos las matrices usando `ExecutorService` y su método **ejecutar** pasando una instancia de la tarea `MatrixMultiplicationTask`.

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
En el código anterior básicamente hicimos:

1. Definir las matrices que vamos a multiplicar. 
2. Calcular la cantidad total de subprocesos necesarios para la multiplicación (que es la cantidad de elementos en la matriz de resultados) y crear un grupo(pool) de subprocesos fijos con ese tamaño utilizando **Executors.newFixedThreadPool(numThreads)**. 
3. Iterar sobre cada elemento en la matriz de resultados y enviar una tarea de tipo `MatrixMultiplicationTask` al ejecutor para su ejecución. 
4. Al enviar todas las tareas, llamamos a **executor.shutdown()** para iniciar el apagado correcto del ejecutor. 
5. Finalmente, esperamos a que se completen todas las tareas comprobando **executor.isTerpressed()** e imprimimos la matriz resultante. 

## Conclusión
Executor Framework en Java proporciona una abstracción de alto nivel para administrar subprocesos y simplifica la creación de aplicaciones multi-hilos. Sus componentes clave, como las interfaces Executor y ExecutorService, junto con las clases ThreadPoolExecutor y Executors, permiten a los desarrolladores administrar de manera eficiente la ejecución de subprocesos. Al utilizar Executor Framework, los desarrolladores pueden aprovechar el poder de los subprocesos múltiples y evitar las complejidades asociadas con la administración manual de hilos.

## Referencias
[Cómo multiplicar matrices](https://www.mathsisfun.com/algebra/matrix-multiplying.html)