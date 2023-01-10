## Introducción
El patrón decorador es un patrón de diseño que le permite agregar nuevas funciones a los objetos existentes de una manera flexible y transparente. Implica crear un nuevo objeto que envuelva el objeto original, agregar la nueva funcionalidad al contenedor y luego devolver el contenedor en lugar del objeto original.

## Diagrama UML
Aquí hay un diagrama que ilustra el patrón del decorador:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1AEYMal_DTjLNyJn4zLhL1WanPGFpsdkc)

El patrón decorador tiene los siguientes componentes:

1. **Component**: Esta es la interfaz que define los métodos que debe implementar el objeto que se está decorando.
2. **ConcreteComponent**: esta es una implementación concreta de la interfaz del componente. Representa el objeto que se está decorando.
3. **Decorator**: esta es una clase abstracta que implementa la interfaz del componente y tiene un campo para almacenar una referencia al componente que se está decorando. También tiene un constructor que toma un componente como argumento e inicializa el campo con el componente.
4. **ConcreteDecorator**: Esta es una implementación concreta de la clase decorador. Agrega un nuevo comportamiento al componente que se está decorando al implementar los métodos definidos en la interfaz del componente.

## El problema
Imagine que está creando una aplicación de software que permite a los usuarios dibujar diferentes tipos de formas en la pantalla, como círculos, cuadrados, triángulos, etc. Ha implementado una interfaz `Shape` que define un método `draw()` y ha creado implementaciones concretas de esta interfaz para cada uno de los diferentes tipos de formas.

Ahora, desea permitir que los usuarios agreguen varios tipos de decoraciones a las formas que dibujan, como cambiar el color del borde, agregar una sombra paralela o rellenar la forma con un degradado. Puede usar el patrón decorador para agregar esta funcionalidad a su aplicación de una manera flexible y transparente.

## La solución
Así es como podría implementar el patrón decorador para resolver este problema:

1. Defina la interfaz `Shape` y cree implementaciones concretas para cada uno de los diferentes tipos de formas.
2. Cree una clase `ShapeDecorator` abstracta que implemente la interfaz `Shape` y tenga un campo para almacenar una referencia al objeto `Shape` que se está decorando.
3. Crea clases de decoradores concretas para cada tipo de decoración que quieras apoyar. Cada clase de decorador debe extender la clase `ShapeDecorator` y anular el método **draw()** para agregar la decoración deseada a la forma.
4. Para aplicar una decoración a una forma, cree una instancia de la clase decorador y pase la forma que se va a decorar como argumento al constructor del decorador.

### Diagrama de la solución
A continuación tenemos el diagrama que representa nuestra solución en UML:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1rBrpRoOd4thzHWpUrK0P3RQDbucppp3w)

Con este enfoque, puede agregar nuevos tipos de decoraciones a su aplicación simplemente creando nuevas clases de decoradores, sin tener que cambiar la implementación de las formas decoradas(`Circle` y `Rectangle`).

## Implementación Java
Aquí hay un ejemplo de cómo podemos implementar el patrón decorador en Java:

### Interfaz de Shape y clases concretas
````java
public interface Shape {
  void draw();
}

public class Circle implements Shape {
  @Override
  public void draw() {
    System.out.println("Drawing a circle");
  }
}

public class Rectangle implements Shape {
  @Override
  public void draw() {
    System.out.println("Drawing a rectangle");
  }
}
````

### Entidades decoradoras
````java
public abstract class ShapeDecorator implements Shape {
  protected Shape decoratedShape;

  public ShapeDecorator(Shape decoratedShape) {
    this.decoratedShape = decoratedShape;
  }

  @Override
  public void draw() {
    decoratedShape.draw();
  }
}

public class RedShapeDecorator extends ShapeDecorator {
  public RedShapeDecorator(Shape decoratedShape) {
    super(decoratedShape);
  }

  @Override
  public void draw() {
    decoratedShape.draw();
    setRedBorder(decoratedShape);
  }

  private void setRedBorder(Shape decoratedShape) {
    System.out.println("Setting border color to red");
  }
}
````

### La clases Main:

````java
public class Main {
  public static void main(String[] args) {
    Shape circle = new Circle();
    Shape redCircle = new RedShapeDecorator(new Circle());
    Shape redRectangle = new RedShapeDecorator(new Rectangle());
    circle.draw();
    redCircle.draw();
    redRectangle.draw();
  }
}
````

La salida del código anterior es:

````commandline
Drawing a circle
Drawing a circle
Setting border color to red
Drawing a rectangle
Setting border color to red
````

### Conclusión
En este tutorial, aprendimos cómo el patrón decorador le permite agregar nuevas funciones a los objetos existentes de una manera flexible y transparente, sin cambiar la implementación de los objetos que se decoran. Hemos expuesto el problema junto con la solución y su implementación en Java. Gracias por pasar.

¡Feliz código!