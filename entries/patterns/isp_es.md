## Introducción
El principio de segregación de interfaz (ISP) es un principio de programación orientada a objetos que establece que los clientes no deben verse obligados a depender de interfaces que no utilizan. Es uno de los principios **SOLID** del diseño orientado a objetos.

El principio establece que es mejor tener muchas interfaces pequeñas y específicas en lugar de unas pocas grandes y generales. Esto ayuda a reducir la cantidad de dependencias innecesarias entre clases y permite una mayor flexibilidad y modularidad en el diseño.

## El problema
Imagine que está diseñando un sistema para una empresa que gestiona una flota de camiones de reparto. Cada camión tiene una serie de sensores que recopilan datos sobre la ubicación del camión, el nivel de combustible, la presión de los neumáticos y otras métricas importantes. A continuación puedes ver el diseño de este sistema:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1bg49UlmiK3a1BMCxLkYkyKSeCQw7UucK)

En este ejemplo, la interfaz `Trackable` tiene seis métodos: **getLatitude()**, **getLongitude()**, **getFuelLevel()**, **getTirePressure()**, **addFuel() **, y **inflarTires()**. La clase `DeliveryTruck` implementa esta interfaz y proporciona su propia implementación de estos métodos. A primera vista, todo parece estar bien, además del notable alto acoplamiento en la interfaz `Trackable`.

Ahora, la empresa decidió volverse más ecológica y respetuosa con el medio ambiente, por lo que el próximo lote de camiones será eléctrico y, obviamente, se integrarán en nuestro sistema para que podamos rastrearlos. Nuestra primera y rápida solución es introducir un nuevo modelo para coches eléctricos e implementar la interfaz `Trackable`, así es como se ve el diseño después de introducir la clase `ElectricTruck`:

![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1QUPIXvg7LmDF4nAeOXk295oFJrf1cMT-)

Fíjate bien... ¿hay algo que te suene? ¡Absolutamente, el diagrama nos dice que los autos eléctricos son compatibles con el sistema de combustible!
Algunos de los problemas de este enfoque:

1. **Acoplamiento estrecho**: Las clases `DeliveryTruck` y `ElectricTruck` están fuertemente acopladas a la interfaz ``Trackable``, lo que significa que están estrechamente vinculadas a esta interfaz y no se pueden usar sin ella. Esto puede hacer que el diseño sea inflexible, difícil de modificar y testear.
2. **Dependencias innecesarias**: La clase `ElectricTruck` no necesita implementar los métodos **getFuelLevel()** y **addFuel(doble cantidad)**, sino que se ve obligada a hacerlo debido a el contrato indicado en la interfaz `Trackable`. Esto crea una dependencia innecesaria.
3. **Falta de modularidad**: La interfaz `Trackable` es una interfaz grande y general que tiene métodos para varios propósitos. Esto puede dificultar la comprensión y el uso de la interfaz, y puede dificultar aún más la adición de nuevos métodos o la realización de cambios en la interfaz.
4. **Escasa separación de concern**: la interfaz `Rastreable` mezcla preocupaciones para calcular la posición geográfica, los niveles de combustible y la presión de los neumáticos de una entidad "Rastreable". Esto puede hacer que la interfaz sea más compleja y difícil de reutilizar.

## La solución
De acuerdo con el principio de segregación de interfaces, sería mejor tener interfaces separadas para los diferentes aspectos de un camión. Por ejemplo, podría tener una interfaz `LocationTracker` con métodos para obtener la latitud y la longitud del camión, una interfaz `FuelSystemTracker` con métodos para obtener el nivel de combustible y agregar combustible al camión, y `TireSystemTracker ` para obtener la presión de los neumáticos e inflarlos. Esto permitiría que nuestra clase `ElectricTruck` solo implemente las interfaces que necesita, en lugar de verse obligada a implementar todos los métodos en la interfaz `Trackable`.
### Solution diagram
![New Project using PyCharm](https://drive.google.com/uc?export=view&id=1DrnwoL8Vt8C2GGW_KMWT2gOin845ddYC)

En el diseño anterior, la clase `DeliveryTruck` implementa tres interfaces separadas: `LocationTracker`, `FuelSystemTracker` y `TireSystemTracker`. Esto permite que la clase solo dependa de los métodos que necesita, en lugar de verse obligada a implementar todos los métodos desde la interfaz `Trackeable`. Esto es más obvio en la clase `ElectricTruck` ya que no es compatible con el sistema de combustible y no implementa la interfaz `FuelSystemTracker`.

## Implementación
Aquí está la implementación usando Java, la clase `DeliveryTruck`:

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

Y la clase `ElectricTruck`, que solo implementa las interfaces `LocationTracker` y `TireSystemTracker`, porque no tiene un sistema de combustible y, por lo tanto, no puede rastrear su nivel de combustible. Esto permite que la clase solo dependa de los métodos que necesita, en lugar de verse obligada a implementar un comportamiento innecesario:

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