## Introduction
The decorator pattern is a design pattern that allows you to add new functionality to existing objects in a flexible and transparent way. It involves creating a new object that wraps the original object, adding the new functionality to the wrapper, and then returning the wrapper in place of the original object.

## UML Diagram
Here is a diagram illustrating the decorator pattern:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1AEYMal_DTjLNyJn4zLhL1WanPGFpsdkc)

The decorator pattern has the following components:

1. **Component**: This is the interface that defines the methods that the object being decorated must implement.
2. **ConcreteComponent**: This is a concrete implementation of the component interface. It represents the object being decorated.
3. **Decorator**: This is an abstract class that implements the component interface and has a field for storing a reference to the component being decorated. It also has a constructor that takes a component as an argument and initializes the field with the component.
4. **ConcreteDecorator**: This is a concrete implementation of the decorator class. It adds new behavior to the component being decorated by implementing the methods defined in the component interface.

## The problem
Imagine that you are building a software application that allows users to draw different types of shapes on the screen, such as circles, squares, triangles, and so on. You have implemented a `Shape` interface that defines a `draw()` method, and you have created concrete implementations of this interface for each of the different types of shapes.

Now, you want to allow users to add various types of decorations to the shapes they draw, such as changing the border color, adding a drop shadow, or filling the shape with a gradient. You could use the decorator pattern to add this functionality to your application in a flexible and transparent way.

## The solution
Here is how you could implement the decorator pattern to solve this problem:

1. Define the `Shape` interface and create concrete implementations for each of the different types of shapes.
2. Create an abstract `ShapeDecorator` class that implements the `Shape` interface and has a field for storing a reference to the `Shape` object being decorated.
3. Create concrete decorator classes for each type of decoration you want to support. Each decorator class should extend the `ShapeDecorator` class and override the **draw()** method to add the desired decoration to the shape.
4. To apply a decoration to a shape, create an instance of the decorator class and pass the shape to be decorated as an argument to the decorator's constructor.

### Solution diagram
Below we have the diagram representing our solution in UML:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1rBrpRoOd4thzHWpUrK0P3RQDbucppp3w)

Using this approach, you could add new types of decorations to your application by simply creating new decorator classes, without having to change the implementation of the decorated shapes.

## Java implementation
Here it is an example of how we can implement the decorator pattern in Java:

### Shape interface and classes
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

### Decorator entities
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

### The Main class:

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

The output of the above code is:

````commandline
Drawing a circle
Drawing a circle
Setting border color to red
Drawing a rectangle
Setting border color to red
````

### Conclusion
In this tutorial we learned how the decorator pattern allows you to add new functionality to existing objects in a flexible and transparent way, without changing the implementation of the objects being decorated. We have exposed the problem along with the solution and its implementation in Java. Thanks for stopping by.

Happy code!