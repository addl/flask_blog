## Introducción
En este artículo, aprenderá los conceptos fundamentales de la recolección de basura en Java (aka GC, del ingl&eacute;s Garbage Collector).
Explicaré qué es la recolección de basura y su importancia para la salud de las aplicaciones Java.
También describimos los diferentes procesos como el marcado de objetos y las diferentes generaciones en las que se divide el *heap*.
Finalmente, se explica los tipos de recolectores de basura y herramientas para monitorear el *heap* y la actividad de aplicaciones Java en ejecuci&oacute;n.

## ¿Qué es la recolección de basura?
En un lenguaje de programación como C, la asignación y desasignación de memoria es un proceso manual.
En Java, el recolector de basura maneja automáticamente el proceso de desasignación de memoria.

La recolección automática de objetos no utilizados es el proceso de observar el *heap*, identificar qué objetos se están utilizando y cuáles no, y proceder con la eliminación de los objetos no utilizados.
Un objeto en uso, o un objeto al que se hace referencia, significa que alguna parte de su programa aún mantiene un puntero a ese objeto.
Por otro lado, o un objeto sin referencia, significa que el código de su programa ya no hace referencia a este objeto, por lo que la memoria utilizada por estos objetos sin referencia puede recuperarse.
En pocas palabras, la recolección de basura es un proceso para liberar memoria.

## Relevancia de la recolección de basura
La recolección de basura en Java libera al programador de lidiar manualmente con la desasignación de memoria.
Como resultado, GC elimina o reduce sustancialmente ciertos errores como:  

* Errores de punteros colgantes, que ocurren cuando se libera una parte de la memoria mientras todavía hay punteros hacia ella, y se elimina la referencia de uno de esos punteros. Para entonces, la memoria puede haber sido reasignada a otro uso con resultados impredecibles.
* Errores de doble liberación, que ocurren cuando el programa intenta liberar una región de memoria que ya ha sido liberada y quizás ya ha sido asignada nuevamente.
* Ciertos tipos de fugas de memoria, en las que un programa no puede liberar la memoria ocupada por objetos que se han vuelto inalcanzables, lo que puede provocar el agotamiento de la memoria.


## Proceso de marcado (marking)
El primer paso en la recolección de basura se llama marcado o **marking**.
Aquí es donde el recolector de basura identifica qué piezas de memoria están en uso y cuáles no, la siguiente imagen brinda más detalles:

![Garbage Collector Marking Process](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/gcslides/Slide3.png)

Los objetos a los que se hace referencia se muestran en azul. Los objetos sin referencia se muestran en dorado.
Todos los objetos se escanean en la fase de marcado para hacer esta determinación.
Este proceso de 'marcar' puede consumir mucho tiempo y volverse ineficiente a medida que los objetos en un sistema siguen creciendo y creciendo.

## Clasificación de generación de objetos
El análisis empírico de las aplicaciones ha demostrado que la mayoría de los objetos son de corta duración, eche un vistazo al siguiente gráfico:

![Object Usage over time in JVMs](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/ObjectLifetime.gif)

Como puede ver, quedan menos objetos referenciados a lo largo del tiempo. De hecho, la mayoría de los objetos tienen una vida muy corta, como lo muestran los valores más altos en el lado izquierdo del gráfico.

La información anterior se ha utilizado para mejorar el proceso de recolección de basura en la JVM; por lo tanto, la memoria *heap* se ha dividido en varias áreas, como se muestra en la siguiente imagen:  

![Heap Generations](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/gcslides/Slide5.png)

### Young generation
En la generación joven, todos los objetos nuevos se asignan y envejecen en el área de generación joven. Cuando esta área se llena, se ejecuta una `minor garbage collection`.
Las colecciones menores se pueden optimizar asumiendo una alta tasa de mortalidad de objetos. Una generación joven llena de objetos muertos se recoge muy rápidamente.
Algunos objetos sobrevivientes envejecen y eventualmente pasan a la generación vieja u *old generation*.


### Old generation
La generación vieja, esta zona se utiliza para almacenar objetos de larga supervivencia.
Por lo general, se establece un umbral para los objetos de la generación joven y, cuando se alcanza esa edad, el objeto se traslada a la generación vieja.
Eventualmente, la vieja generación necesita ser recolectada. Este evento se denomina `major garbage collection`.

A menudo, una *major garbage collection* es mucho más lenta porque involucra todos los objetos vivos.
Por lo tanto, para las aplicaciones receptivas, se deben minimizar este tipo de recolección.


### The Permanent generation
Finalmente, la generación permanente contiene metadatos requeridos por la JVM para describir las clases y métodos utilizados en la aplicación.
La JVM completa la generación permanente en tiempo de ejecución en función de las clases que usa la aplicación.
Además, las clases y los métodos de la biblioteca Java SE pueden almacenarse aquí.

Las clases pueden recopilarse (descargarse) si la JVM descubre que ya no son necesarias y es posible que se necesite espacio para otras clases.
La generación permanente está incluida en un `full garbage collection` o recolección de basura completa.

> Para realizar una recolección de basura, ya sea menor, mayor o completa, la JVM debe detener la ejecución de la aplicación durante al menos un breve período de tiempo. Este proceso se llama **stop-the-world**, que se traduce como "parar al mundo".
> Esto significa que todos los subprocesos, excepto los subprocesos del GC, dejarán de ejecutarse hasta que se ejecuten los subprocesos del GC y el recolector de basura libere los objetos.
 

## Supervisión de la memoria HEAP
Ahora que conocemos las diferentes áreas en que se divide el heap de la JVM, podemos inspeccionarlo por nuestra cuenta. 
Usaré VisualVM, una herramienta visual que brinda capacidades de generación de perfiles para las actividades de la JVM.
Hay muchas otras herramientas de creación de perfiles convencionales.
Sin embargo, VisualVM es gratuito y viene incluido con las versiones de JDK 6,7 y 8.
Para otras versiones de Java, como 1.9+, Java VisualVM está disponible como [aplicación independiente](https://visualvm.github.io/).

En mi caso he instalado Java 1.8, por lo que tengo VisualVM en el directorio bin de mi instalación de JDK:`C:\Program Files\Java\jdk-11.0.12\bin`, el archivo es: `jvisualvm.exe`, así que por simplemente haciendo doble clic en él, tengo la herramienta en funcionamiento.

![Visual VM tool](https://drive.google.com/uc?id=1G_eD8tNn2RHbRup-Zbqa-UEI_ZCrx7_u)

Como puede ver, enumera todas las aplicaciones Java que se ejecutan actualmente, por ejemplo, yo tengo abierto en mi PC a PyCharm y Eclipse.
Como estamos buscando inspeccionar el *heap*, necesitamos instalar un módulo llamado `VisalGC`.
Así que hagamos clic en el menú: **Tool/Herramientas** --> **Plugins/Complementos**, luego abramos la pestaña **Available plugins/Complementos disponibles** e instálelo, más detalles en la siguiente figura:

![Heap Generations](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/images/visualvm/VisualGCIns02.png)

Después de completar el asistente, deberíamos recibir un mensaje exitoso que significa que la instalación se completó.

### Analizar una aplicación
Ahora analicemos mi instancia de Eclipse, desde la página de inicio de VisualVM, haré clic derecho en la aplicación Eclipse en la lista de aplicaciones locales de la pestaña Aplicaciones y luego seleccionaré **Abrir**.
Observe que se cargan varias pestañas en el lado derecho de la interfaz. Iré a la pestaña **Visual GC** y puedo ver la siguiente interfaz:

![Visual VM tool](https://drive.google.com/uc?id=1UJxRsEImGCoaUuds_2PethVXjXdCUyrj)

Si realizo una tarea en Eclipse, por ejemplo, realizando una búsqueda de cadenas en mi espacio de trabajo, noto rápidamente cómo afecta los gráficos y las métricas.
Siéntase libre de probar las otras pestañas y ver qué información se presenta sobre la JVM.

## Formas de realizar la recolección de basura

La JVM de Oracle HotSpot tradicional tiene cuatro formas de realizar la actividad de recolección de basura:

### GC en serie
El recopilador en serie es el predeterminado para las máquinas de estilo cliente, donde solo un subproceso ejecutó el GC.
Con el recolector en serie, las recolecciones de basura mayores y menores se realizan en serie (utilizando una única CPU virtual). De ahí su nombre.

Serial GC utiliza un método de recopilación **mark-compact**.
Este método mueve la memoria más antigua al principio del *heap* para que las nuevas asignaciones de memoria se conviertan en un único fragmento continuo de memoria al final del *heap*.
Esta compactación de la memoria hace que sea más rápido asignar nuevos fragmentos.

Para habilitar el Serial Collector puede usar la opción: `-XX:+UseSerialGC`, por ejemplo:
````commandline
java -XX:+UseSerialGC -jar c:\javademos\demo\jfc\Java2D\Java2demo.jar
````
Un uso común para Serial GC es en entornos donde se ejecuta una gran cantidad de JVM en la misma máquina (en algunos casos, ¡más JVM que procesadores disponibles!).
En tales entornos, cuando una JVM realiza una recolección de elementos no utilizados, es mejor usar solo un procesador para minimizar la interferencia con las JVM restantes, incluso si la recolección de elementos puede durar más.

### GC en paralelo
El recolector de basura paralelo utiliza varios subprocesos para realizar la recolección de basura de generación joven.
De forma predeterminada, en un host con N CPU, el recolector de basura en paralelo utiliza N subprocesos de recolección de elementos no utilizados en la colección.
La cantidad de subprocesos del recolector de elementos no utilizados se puede controlar con las opciones de la línea de comandos: `-XX:ParallelGCThreads=<número deseado>`

El recolector paralelo también se denomina recolector de rendimiento. Ya que puede usar múltiples CPU para acelerar el rendimiento de la aplicación.
Básicamente, podemos ejecutar el recolector de basura paralelo en dos modos: 

1. Un recopilador de generación joven de subprocesos múltiples con un recopilador de generación anterior de subproceso único: `-XX:+UseParallelGC`.
2. Tanto un recopilador de subprocesos múltiples de generación joven como un recopilador de subprocesos múltiples de generación anterior: `-XX:+UseParallelOldGC`.


### Concurrent Mark Sweep (CMS)
El Barrido de marcas simultáneo es similar al paralelo, también permite la ejecución de algunos subprocesos de aplicación y reduce la frecuencia de parada del mundo.
Intenta minimizar las pausas debidas a la recolección de objetos no utilizados realizando la mayor parte del trabajo de recolección simultáneamente con los subprocesos de la aplicación.
Normalmente, este proceso no compacta los objetos activos, por lo que se realiza una recolección de basura sin mover los objetos vivos.
En este caso, si la fragmentación se convierte en un problema, el proceso asigne un espacio más grande de memoria al *heap*.

> El colector CMS en generación joven utiliza el mismo algoritmo que el colector en paralelo.

El recolector de CMS debe usarse para aplicaciones que requieren tiempos de pausa bajos y pueden compartir recursos con el recolector de basura.
Los ejemplos incluyen aplicaciones de interfaz de usuario de escritorio que responden a eventos, un servidor web que responde a una solicitud o una base de datos que responde a consultas.

Para habilitar el uso de CMS Collector: `-XX:+UseConcMarkSweepGC` y para establecer el número de subprocesos, use: `-XX:ParallelCMSThreads=<n>`.

### G1
G1 se ejecuta en paralelo y concurrentemente como CMS, pero funciona de manera diferente a CMS y está diseñado para ser el reemplazo a largo plazo del recopilador CMS.
El recolector G1 es un recolector de basura de baja pausa, concurrente y de compactación incremental que tiene un diseño bastante diferente a los otros recolectores de basura descritos en esta publicación.
En entradas posteriores, describiré en detalle cómo funciona.

Para habilitar el uso de G1 Collector: `-XX:+UseG1GC`.

Curiosamente, echando un vistazo a la instancia de mi Eclipse de VisualVM, se ejecuta con G1:
````commandline
-Dosgi.requiredJavaVersion=11
-Dosgi.instance.area.default=@user.home/eclipse-workspace
-XX:+UseG1GC
````

> Modern JVMs like Azul Zing use Continuously Concurrent Compacting Collector (C4), which eliminates the stop-the-world GC pauses, thus increasing the scalability.

## Conclusión
En esta entrada, hemos aprendido los fundamentos de la recolección de basura de Java al presentar las diferentes áreas del montón de memoria y la importancia de que este proceso se ejecute automáticamente.
También explicamos el proceso de marcado y la clasificación de generaciones dentro del *heap*. Hemos visto VisualVM, una herramienta importante para monitorear la ejecución de aplicaciones Java.
Finalmente, aprendimos las diferentes formas en que se ejecuta la recolección de basura.

## reference

[Webfolder technetwork in Oracle](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/index.html)

[Java technotes](https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/sizing.html#heap_parameters)

[Docs Oracle Collectors](https://docs.oracle.com/javase%2F8%2Fdocs%2Ftechnotes%2Fguides%2Fvm%2Fgctuning%2F%2F/collectors.html)
