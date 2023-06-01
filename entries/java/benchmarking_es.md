## poster
![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1Y3RF8GlqW6qn_S3C8fFjZvoNHmnPE1pR)

## Introducción
JMH (Java Microbenchmark Harness) es una poderosa herramienta de evaluación comparativa utilizada para medir el rendimiento del código Java.
Proporciona un enfoque confiable y estandarizado para la evaluación comparativa, lo que permite a los desarrolladores evaluar con precisión las características de rendimiento de su código. En este blog, exploraremos las características y el uso de JMH, junto con las mejores prácticas para evaluar comparativamente las aplicaciones Java.

## Por qué usar JMH
JMH ofrece varias ventajas para la evaluación comparativa del código Java:

* Evaluación comparativa estandarizada: JMH proporciona un marco estandarizado para la evaluación comparativa del código Java, lo que garantiza resultados consistentes y confiables en diferentes entornos. 
* Medición precisa: JMH se ocupa de varios factores que pueden afectar los resultados de la evaluación comparativa, como el calentamiento de JVM, la compilación Just-In-Time (JIT) y la sincronización de subprocesos. Esto garantiza una medición precisa del rendimiento del código. 
* Modos de referencia: JMH admite diferentes modos de referencia, incluidos el rendimiento, el tiempo promedio y el tiempo de muestra. Estos modos le permiten concentrarse en aspectos de rendimiento específicos según sus requisitos. 
* Parametrización: JMH admite la parametrización de puntos de referencia, lo que le permite probar su código con diferentes escenarios de entrada. Esto ayuda a identificar variaciones de rendimiento y optimizar su código en consecuencia. 
* Integración con generadores de perfiles: JMH se integra a la perfección con generadores de perfiles y herramientas de diagnóstico como Java Flight Recorder (JFR) y JMH-profiler. Esto permite un análisis en profundidad de los resultados de referencia para identificar cuellos de botella en el rendimiento y optimizar el código. 

Antes de profundizar en la codificación de los benchmarks, debemos comprender sus elementos claves.

## La anotación Benchmark
Usamos la anotación `@Benchmark` proporcionada por JMH para marcar los métodos que desea comparar. JMH ejecutará estos métodos y medirá su desempeño.

```java
@Benchmark
public void myRoutineToComputeSomething() {
    // Code to be benchmarked
}
```

## Tipos de benchmarks
Hay cuatro tipos diferentes de benchmarks disponibles:

1. Mode.AverageTime: Mide el tiempo promedio que toma cada operación. 
2. Mode.SampleTime: tiempo para cada operación, incluidos min y max. 
3. Mode.SingleShotTime: Tiempo para una sola operación. 
4. Mode.Throughput: Mide el número de operaciones por unidad de tiempo. 
5. Mode.All: Todo lo anterior. 

Podemos establecer los modos deseados con la anotación `@BenchmarkMode(...)`. El modo predeterminado es `Mode.Throughput`.

## Control del calentamiento y la medición
Las iteraciones de calentamiento permiten que la JVM alcance un estado estable antes de que comiencen las mediciones. Las iteraciones de medición se utilizan para recopilar los datos de referencia.
Puede configurar el número de iteraciones de calentamiento y medición utilizando las anotaciones `@Warmup` y `@Measurement`, por ejemplo:

```java
@Benchmark
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public void myRoutineToComputeSomething() {
    // Code to be benchmarked
}
```
La configuración anterior ejecuta tres iteraciones de calentamiento seguidas de cinco iteraciones de medición.

## Configuración y estado de los puntos de referencia
La clase marcada con `@State` puede contener campos que representan las variables de estado requeridas para el benchmar y/o inicialización mediante el uso de métodos anotados con `@Setup`. Por ejemplo:

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
El método **setup()** se llamará una vez antes de cada iteración de un benchmark para configurar su estado inicial.

## Puntos de referencia parametrizados
JMH admite la parametrización de los benchmarks para inicializar los diferentes parámetros.
Esto se puede lograr usando la anotación `@Param`:

```java
@State(Scope.Benchmark)
public static class BenchmarkState {
    @Param({"10"})
    public int number;
}
```

El valor de la variable `number` se especifica en la anotación `@Param`.


## Creando el proyecto maven
La forma más sencilla de ejecutar los benchmarks de JMH es crear un proyecto maven usando los arquetipos de JMH, podemos generar el proyecto desde la línea de comandos o usando cualquier IDE.

### Usando la línea de comando
Para generar el proyecto maven desde la línea de comando, ejecute el comando:

```commandline
$ mvn archetype:generate -DinteractiveMode=false -DarchetypeGroupId=org.openjdk.jmh \
    -DarchetypeArtifactId=jmh-java-benchmark-archetype -DgroupId=com.myrefactor \
    -DartifactId=benchmarking -Dversion=1.0
```

### Uso del IDE de Eclipse
Simplemente, cree un nuevo proyecto maven desde el menú Archivo -> Nuevo -> Proyecto Maven y asegúrese de ingresar el arquetipo de la siguiente manera:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1Y2QuEM7Ek7WByxWLQqAg6PB9sIQJ_XXx)


En ambos casos terminará con un proyecto y una clase principal llamada `MyBenchmark`, con el siguiente contenido:
```java
public class MyBenchmark {

    @Benchmark
    public void testMethod() {
        // This is a demo/sample template for building your JMH benchmarks. Edit as needed.
        // Put your benchmark code here.
    }
    
}
```
Modificaremos esta clase y crearemos un benchmark para un algoritmo de la serie de Fibonacci. 

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
El código anterior envuelve la ejecución del método **computeFibonacciLoop** dentro del método **testMethod**. Esto es útil para aislar el método que queremos testear y la configuración del benchmark.

## Ejecutando los puntos de referencia
Una vez que su benchmark esté listo para ejecutarse. Debemos construirlo con el siguiente comando:
```commandline
$ mvn clean verify
```

Una vez finalizada la compilación, obtendrá el archivo JAR ejecutable, que contiene el benchmark, y ejecutamos:
```commandline
java -jar target/benchmarks.jar
```
> Observe cómo el archivo `jar` generado se llama `benchmarks.jar`, este es el resultado de crear el proyecto con el archetype de JMH en maven.

La salida será:

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

## Resultados
La interpretación de los resultados requiere la comprensión de varias métricas:

* Throughput(Rendimiento): Representa el número de operaciones ejecutadas por unidad de tiempo. Los valores de rendimiento más altos indican un mejor rendimiento. 
* Average Time(Tiempo Promedio): Representa el tiempo promedio de cada operación. Los valores de tiempo promedio más bajos indican un mejor rendimiento. 
* Percentiles: Proporciona información sobre la distribución de tiempos. Por ejemplo, el percentil 99 indica el tiempo por debajo del cual cae el 99% de los valores medidos. Los percentiles ayudan a identificar valores atípicos y posibles problemas de rendimiento. 


### Interpretación de resultados
Estas métricas deben analizarse para identificar cuellos de botella en el rendimiento y áreas de optimización. En nuestra salida de ejemplo:

1. El benchmark logró un rendimiento de aproximadamente 1,915,365,597.778 operaciones por segundo, con un margen de error de 89,718,491.176 ops/s. El "? (99,9%)" indica que este es el intervalo de confianza. 
2. Las puntuaciones mínimas, medias y máximas observadas durante las ejecuciones comparativas fueron 1,473,967,335.788 ops/s, 1,915,365,597.778 ops/s, y 2,090,416,921.603 ops/s, respectivamente. 
3. La desviación estándar (stdev) de las puntuaciones es 119.771.618,852 ops/s. Una desviación estándar más alta sugiere que los puntajes de referencia tienen un mayor grado de variabilidad o dispersión. 


## Buenas prácticas y consejos
Aquí hay algunos consejos para la implementación efectiva de benchmarks:

* Estrategias de calentamiento: diseñe estrategias de calentamiento adecuadas para permitir que la JVM alcance un estado optimizado antes de que comiencen las mediciones. Esto garantiza resultados estables y precisos. 
* Opciones de JVM: configure las opciones de JVM, como el tamaño del heap y la configuración del recolector de basura, para garantizar un rendimiento óptimo durante la evaluación. 
* Evite errores comunes: errores comunes son la eliminación de código inactivo y la incorporación de métodos por parte del compilador JIT. Utilice anotaciones específicas de JMH como `@CompilerControl` o `@BenchmarkMode(Mode.SingleShotTime)` para mitigar estos problemas. 
* Céntrate en métodos únicos: aplica los benchmarks a métodos individuales en lugar de componentes o sistemas completos. Esto proporciona resultados enfocados y permite una optimización específica. 
* Valide y verifique los resultados: valide los resultados por medio de ejecutar múltiples iteraciones y verificando la consistencia. Asegúrese de que cualquier mejora en el rendimiento sea estadísticamente significativa. 

## Solución de problemas
### No usar el arquetipo
Durante mis tests, recibí el siguiente error cuando intento configurar un proyecto de Eclipse sin usar el arquetipo y especificando las dependencias manualmente en `pom.xml`.

```commandline
ERROR: Unable to find the resource: /META-INF/BenchmarkList
```
Se recomienda generar el proyecto utilizando el arquetipo.

### Procesamiento de anotaciones
JMH encuentra sus métodos de referencia anotados con `@Benchmark`, debe habilitar el procesamiento de anotaciones en su IDE, de lo contrario, se encontrará con el siguiente error:

```commandline
No benchmarks found, skipping.
```

## Conclusión
En esta publicación, exploramos las funciones y el uso de JMH (Java Microbenchmark Harness) para evaluar comparativamente el código Java. Discutimos la importancia de usar JMH para una medición precisa del rendimiento y cubrimos temas como configurar JMH, implementamos un benchmark usando un algoritmo de Fibonacci como ejemplo, controlamos el calentamiento y la medición, usamos parámetros por medio del estado y analizamos el resultado del test. Finalmente, cubrimos algunas de las mejores prácticas para una evaluación comparativa efectiva.

## Referencias

[JMH Official Website](https://github.com/openjdk/jmh)

[Microbenchmarks With JMH](https://blog.avenuecode.com/java-microbenchmarks-with-jmh-part-1)

[Architect Benchmarking](https://www.oracle.com/technical-resources/articles/java/architect-benchmarking.html)