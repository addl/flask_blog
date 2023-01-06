# Visi&oacute;n general
En esta entrada, cubrir&eacute; todos los tipos de Pointcut Designators tambi&eacute;n llamados PCD compatibles con Spring AOP.
Adem&aacute;s, proporcionar&eacute; explicaciones y ejemplos para cada uno de ellos.

# Introducci&oacute;n
Para comprender PCD, necesitamos conocer la naturaleza de Spring AOP y su diferencia con AspectJ.
De la documentaci&oacute;n de Spring:
> Debido a la naturaleza basada en proxy del marco AOP de Spring, los m&eacute;todos protegidos, por definici&oacute;n, no son interceptados, ni para los proxies JDK (donde esto no es aplicable) ni para los proxies CGLIB (donde esto es t&eacute;cnicamente posible pero no recomendable para fines AOP) . Como consecuencia, cualquier punto de corte dado se comparar&aacute; solo con m&eacute;todos p&uacute;blicos.

Por lo tanto, si su intercepci&oacute;n necesita incluir m&eacute;todos protegidos/privados o incluso constructores, considere el uso del tejido de AspectJ nativo impulsado por Spring en lugar de AOP basado en proxy de Spring. Esto constituye un modo diferente de uso de AOP con diferentes caracter&iacute;sticas, as&iacute; que aseg&uacute;rese de familiarizarse con el tejido antes de tomar una decisi&oacute;n.

Dicho esto, cada ejecuci&oacute;n de m&eacute;todo en Spring AOP se realiza mediante proxy, lo que significa que se ajusta en tiempo de ejecuci&oacute;n para interceptar su ejecuci&oacute;n. Una imagen dice m&aacute;s que palabras (Fuente:[Spring in Action](https://www.amazon.com/Spring-Action-Sixth-Craig-Walls/dp/1617297577/ref=sr_1_4?crid=VPOOX5S4K2UT&keywords=spring+in +acci&oacute;n+3ra+edici&oacute;n&qid=1653372060&sprefix=primavera+en+acci&oacute;n+3ra+edici&oacute;n%2Caps%2C155&sr=8-4)):

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1iHhZXbEnF45sU5ze42k5dbZV08nEr85y)

Ahora procedamos con los diferentes PCD.

## execution
Este PCD se usa para hacer coincidir los puntos de uni&oacute;n de ejecuci&oacute;n del m&eacute;todo, este es el designador de corte de punto principal que usar&aacute; cuando trabaje con Spring AOP.
````java
/*
* Matches all methods inside CustomerService in disregards their signature.
* 
* First wildcard refer to any return type, the second refers to any method name and (..) to any
* parameters.
*/
@Pointcut(value = "execution(* com.myrefactor.aop.aopcookbook.service.CustomerService.*(..))")
private void pointcutAllService() {}
````

## within
Limita la coincidencia para unir puntos dentro de ciertos tipos (simplemente la ejecuci&oacute;n de un m&eacute;todo declarado dentro de un tipo de coincidencia cuando se usa Spring AOP).
````java
/*
* Matches all methods inside ProductService in disregards their signature.
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
Tambi&eacute;n es posible hacer coincidir tipos dentro de cualquier paquete, por ejemplo:
````java
/*
* Matches all methods inside 'service' package.
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*)")
private void pointcutAllService() {}
````

## this and target
### this
El **this** PCD limita la coincidencia con los puntos de uni&oacute;n (la ejecuci&oacute;n de m&eacute;todos cuando se usa Spring AOP) donde la referencia del bean (proxy Spring AOP) es una instancia del tipo dado.

### target
Por su parte **target**, limita la coincidencia con los puntos de uni&oacute;n (la ejecuci&oacute;n de m&eacute;todos cuando se usa Spring AOP) donde el objeto de destino (objeto de aplicaci&oacute;n que se intercepta) es una instancia del tipo dado.

Spring AOP es un sistema basado en proxy y diferencia entre el propio objeto proxy (que est&aacute; vinculado a **this**) y el objeto de destino detr&aacute;s del proxy (que est&aacute; vinculado al **target**).

### el proceso de proxy de Spring
Como sabemos, cada Joinpoint est&aacute; envuelto dentro de un proxy, b&aacute;sicamente, Spring puede crear dos tipos de proxies, repas&eacute;moslos r&aacute;pidamente.  

* Proxy basado en JDK: este mecanismo solo puede representar por interfaz (por lo que su clase de destino necesita implementar una interfaz, que luego tambi&eacute;n es implementada por la clase de proxy
* Proxy basado en CGLIB: en este escenario, Spring crea un proxy mediante subclases, por lo que el proxy se convierte en una subclase de la clase de destino.

La siguiente imagen muestra con m&aacute;s detalle este proceso.

![Elastic Search dependencies and versions](https://drive.google.com/uc?id=1JpJ1S43O6efyMIDaykNebi2BqWxFw6lV)

Ahora que tenemos una idea del proceso de proxy de Spring, supongamos que tenemos el siguiente componente:
````java
@Service
public class ProductServiceImpl implements ProductService {
    ...
}
````
Dado que **ProductServiceImpl** implementa una interfaz, Spring crear&aacute; un proxy JDK, y tanto el proxy como el objeto destino(target) ser&aacute;n instancias de la interfaz *ProductService*. As&iacute; que tanto **this** como **target** funcionar&aacute;n.
````java
/*
* Matches all methods inside inside any class which implements ProductService interface.
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
Equivalente a:
````java
/*
* Matches all methods inside inside any class which implements ProductService interface.
*/
@Pointcut("target(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutCustomerService() {}
````
Entonces, ¿D&oacute;nde est&aacute; la diferencia? Para entenderlo necesitamos conocer otro concepto de AOP: **Introduction**.

### concepto de Introduction o introducci&oacute;n
Una Introducci&oacute;n le da el poder de declarar m&eacute;todos o campos adicionales en nombre de un tipo. Spring AOP le permite introducir nuevas interfaces (y una implementaci&oacute;n correspondiente) a cualquier objeto recomendado.  
Por ejemplo, podr&iacute;a usar una introducci&oacute;n para hacer que un bean implemente una interfaz *IsModified*, para simplificar el almacenamiento en cach&eacute;. 
> Una introducci&oacute;n se conoce como una declaraci&oacute;n entre tipos en la comunidad de AspectJ.

As&iacute; que si en este caso hacemos una introducci&oacute;n de alguna interfaz:
> Solo **this** (el proxy) ser&aacute; una instancia de la interfaz dada.

En el escenario anterior, el uso de **objetivo fallar&iacute;a** para que coincida con la interfaz reci&eacute;n introducida.
En resumen, **this** apunta al `proxy` mientras que **target** apunta al `objeto que est&aacute; siendo proxiado`. Adem&aacute;s, si no est&aacute; usando **Introducci&oacute;n**, no debe preocuparse por cu&aacute;l usar.

## args
Limita la coincidencia con los puntos de uni&oacute;n (la ejecuci&oacute;n de m&eacute;todos cuando se usa Spring AOP) donde los argumentos son instancias de los tipos dados
Veamos un ejemplo de su uso:
````java
/*
* Matches all methods inside ProductService
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService)")
private void pointcutProductService() {}

@Around(value = "pointcutProductService() && args(product)")
public Object aroundMethodReceivingProduct(ProceedingJoinPoint jp, Product product)
  throws Throwable {
    ...
}
````
Podr&iacute;amos usar directamente el par&aacute;metro del Joinpoint.

## @target
Limita la coincidencia con los puntos de uni&oacute;n (la ejecuci&oacute;n de m&eacute;todos cuando se usa Spring AOP) donde la clase del objeto en ejecuci&oacute;n tiene una anotaci&oacute;n del tipo dado
````java
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*) && @target(org.springframework.stereotype.Service)")
private void pointcutForAllServices() {}

@Around(value = "pointcutForAllServices()")
public Object aroundCustomerBean(ProceedingJoinPoint jp) throws Throwable {...}
````
> Please notice how we are using **within** to match all classes inside *service* package, but by using **@target** we explicitly target the classes annotated with *@Service*. 

## @args
Limita la coincidencia con los puntos de uni&oacute;n (la ejecuci&oacute;n de m&eacute;todos cuando se usa Spring AOP) donde el tipo de tiempo de ejecuci&oacute;n de los argumentos reales pasados tiene anotaciones de los tipos dados.
````java
/*
* Matches all methods inside ProductService which receive a parameter object annotated
* with @Deprecated
*/
@Pointcut("this(com.myrefactor.aop.aopcookbook.service.ProductService) && @args(java.lang.Deprecated)")
private void pointcutProductService() {}


@Around(value = "pointcutProductService() && args(product)")
public Object aroundMethodReceivingProduct(ProceedingJoinPoint jp, Product product) {...}
````
He agregado la anotaci&oacute;n al modelo del producto de la siguiente manera:
````java
@Deprecated
public class Product implements Serializable {..}
````

## @within
Limita la coincidencia para unir puntos dentro de tipos que tienen la anotaci&oacute;n dada (la ejecuci&oacute;n de m&eacute;todos declarados en tipos con la anotaci&oacute;n dada cuando se usa Spring AOP)
````java
@Pointcut("@within(org.springframework.stereotype.Repository)")
````
Note que lo anterior es equivalente a:
````java
@Pointcut("within(@org.springframework.stereotype.Repository *)")
````

## @annotation
Limita la coincidencia con los puntos de uni&oacute;n donde el sujeto del punto de uni&oacute;n (m&eacute;todo que se ejecuta en Spring AOP) tiene la anotaci&oacute;n dada
En otras palabras, coincide solo si el m&eacute;todo tiene la anotaci&oacute;n que le damos al PCD.
````java
/*
* Matches all methods inside service package but only if it is annotated with @Auditable
*/
@Pointcut("within(com.myrefactor.aop.aopcookbook.service..*) && @annotation(com.myrefactor.aop.aopcookbook.annotations.Auditable)")
private void pointcutCustomerServiceAuditable() {}
````

Si se pregunta c&oacute;mo implementar la anotaci&oacute;n @Auditable, aqu&iacute; tienes el c&oacute;digo:

````java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Auditable {

}
````

## Conclusi&oacute;n
Hemos cubierto todos los PCD compatibles con Spring AOP y brindamos ejemplos de c&oacute;digo para cada uno de ellos que podr&iacute;an aplicarse en escenarios reales. Adem&aacute;s, hemos cubierto conceptos claves como Proxy e Introducci&oacute;n.

## References
https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/aop.html#aop-pointcuts

https://howtodoinjava.com/spring-aop/aspectj-pointcut-expressions/

https://www.baeldung.com/spring-aop-pointcut-tutorial

https://www.javatpoint.com/spring-boot-aop-after-advice