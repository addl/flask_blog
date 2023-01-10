## Introduction
The interface segregation principle (ISP) is a principle of object-oriented programming that states that clients should not be forced to depend on interfaces they do not use. It is one of the **SOLID** principles of object-oriented design.

The principle states that it is better to have many small, specific interfaces rather than a few large, general ones. This helps to reduce the number of unnecessary dependencies between classes and allows for more flexibility and modularity in the design.

## The problem
Imagine that you are designing a system for a company that manages a fleet of delivery trucks. Each truck has a number of sensors that collect data about the truck's location, fuel level, tire pressure, and other important metrics. Below you can see the design of this system:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1bg49UlmiK3a1BMCxLkYkyKSeCQw7UucK)

In this example, the `Trackable` interface has six methods: **getLatitude()**, **getLongitude()**, **getFuelLevel()**, **getTirePressure()**, **addFuel()**, and **inflateTires()**. The `DeliveryTruck` class implements this interface and provides its own implementation of these methods. At first glance, everything seems to be alright, aprt from the noticeable high coupling in the `Trackable` interface.

Now the company decided to become greener and environmentally friendly, so the next batch of truck are electric, and obviously they will be integrated into our system so that we could track them. Our first and quick solution is to introduce a new model for electric cars and implement the `Trackable` interface, here is how the design looks like after introducing the class `ElectricTruck`:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1QUPIXvg7LmDF4nAeOXk295oFJrf1cMT-)

Take a look carefully...is there something that rings a bell? Absolutely, the diagram is telling us that electric cars does support fuel system!
There are a few issues with the first approach:

1. **Tight coupling**: The `DeliveryTruck` and `ElectricTruck` classes are tightly coupled to the `Trackable` interface, which means that they are closely tied to this interface and cannot be used without it. This can make the design inflexible and difficult to modify.
2. **Unnecessary dependencies**: The `ElectricTruck` class does not nees to implement the **getFuelLevel()** and **addFuel(double amount)** methods, but instead it is being forced to do so due to the contract stated in the interface `Trackable`. This creates an unnecessary dependency.
3. **Lack of modularity**: The `Trackable` interface is a large, general interface that has methods for several purposes. This can make the interface difficult to understand and use, and can make it more difficult to add new methods or make changes to the interface.
4. **Poor separation of concerns**: The `Trackable` interface mixes concerns for calculating the geographical position, fuel levels and tires pressure of a `Trackable` entity. This can make the interface more complex and difficult to re-use.

## The solution
According to the interface segregation principle, it would be better to have separate interfaces for the different aspects of a truck. For example, you could have a ``LocationTracker`` interface with methods for getting the latitude and longitude of the truck, a `FuelSystemTracker` interface with methods for getting the fuel level and adding fuel to the truck, and `TireSystemTracker` to get the tire's pressure and inflate them. This would allow our `ElectricTruck` class to only implement the interfaces that it needs, rather than being forced to implement all the methods in the `Trackable` interface.

### Solution diagram
![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1DrnwoL8Vt8C2GGW_KMWT2gOin845ddYC)

In the above design, the `DeliveryTruck` class implements three separate interfaces: `LocationTracker`, `FuelSystemTracker`, and `TireSystemTracker`. This allows the class to only depend on the methods that it needs, rather than being forced to implement all methods from `Trackable` interface. This is more obvious in the `ElectricTruck` class as it doesn't support fuel system and does not implement `FuelSystemTracker`.

## Implementation
Here is the implementation using Java, the `DeliveryTruck` class:

````java
public class DeliveryTruck implements LocationTracker, FuelSystem, TireSystem {
    private GPSSensor gps;
    private FuelSensor fuel;
    private TirePressureSensor tires;
    
    public DeliveryTruck() {
        gps = new GPSSensor();
        fuel = new FuelSensor();
        tires = new TirePressureSensor();
    }
    
    @Override
    public double getLatitude() {
        return gps.getLatitude();
    }
    
    @Override
    public double getLongitude() {
        return gps.getLongitude();
    }
    
    @Override
    public double getFuelLevel() {
        return fuel.getLevel();
    }
    
    @Override
    public void addFuel(double amount) {
        fuel.addFuel(amount);
    }
    
    @Override
    public double getTirePressure() {
        return tires.getPressure();
    }
    
    @Override
    public void inflateTires(double pressure) {
        tires.inflate(pressure);
    }
}

````
And the `ElectricTruck` class, that only implements the `LocationTracker` and `TireSystemTracker` interfaces, because it does not have a fuel system and therefore cannot track its fuel level. This allows the class to only depend on the methods that it needs, rather than being forced to implement unnecessary behavior:
````java
public class ElectricTruck implements LocationTracker, TireSystem {
    private GPSSensor gps;
    private TirePressureSensor tires;
    
    public ElectricTruck() {
        gps = new GPSSensor();
        tires = new TirePressureSensor();
    }
    
    @Override
    public double getLatitude() {
        return gps.getLatitude();
    }
    
    @Override
    public double getLongitude() {
        return gps.getLongitude();
    }
    
    @Override
    public double getTirePressure() {
        return tires.getPressure();
    }
    
    @Override
    public void inflateTires(double pressure) {
        tires.inflate(pressure);
    }
}

````
I hope now you have taken your know-how of this pattern to the next level.

Happy code!

## Conclusion
We have learned how to apply the Interface Segregation Principle by solving a real world scenario. How this SOLID principle can design your classes to be more modular and flexible, allowing the system to be more scalable and adaptable to new requirements.