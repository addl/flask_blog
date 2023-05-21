## poster
![Django vs Flask](https://drive.google.com/uc?export=view&id=122JenjlMwmsojJwiSYtOzTJRr8KjYiO8)

## Introducción
Los marcos web están diseñados para facilitar a los desarrolladores la creación y el mantenimiento de aplicaciones web complejas.
Manejan tareas comunes como el enrutamiento, la representación de plantillas y la interacción con bases de datos.
En esta publicación de blog, compararemos dos de los marcos web más populares para Python, Django y Flask, y lo ayudaremos a comprender cuál es el más adecuado para ti.

## Django
Django es un marco web de pila completa que fue diseñado para ser rápido y flexible. Sigue la filosofía de "baterías incluidas", lo que significa que proporciona una amplia gama de funciones listas para usar para manejar tareas comunes de desarrollo web. Algunas de las características clave de Django incluyen:

### Funciones clave de Django
* **Un ORM (mapeador relacional de objetos)**: Django proporciona un ORM integrado que permite a los desarrolladores trabajar con bases de datos utilizando objetos Python, en lugar de consultas SQL sin formato. El ORM admite una variedad de bases de datos, incluidas PostgreSQL, MySQL y SQLite.
* **Un motor de plantillas robusto para renderizar HTML**: Django proporciona un motor de plantillas que permite a los desarrolladores definir la estructura de sus páginas HTML utilizando el lenguaje de plantillas de Django. El motor de plantillas es muy flexible y admite funciones como herencia, inclusión y etiquetas y filtros personalizados.
* **Un panel de administración incorporado**: Django viene con un poderoso panel de administración que permite a los desarrolladores administrar sus datos a través de una interfaz web intuitiva. El panel de administración es altamente personalizable y se puede ampliar con vistas y acciones personalizadas.
* **Características de seguridad**: Django tiene una serie de características de seguridad integradas para proteger contra ataques comunes como secuencias de comandos entre sitios (XSS) y falsificación de solicitudes entre sitios (CSRF). También brinda soporte para autenticación y permisos de usuarios, lo que permite a los desarrolladores controlar el acceso a sus aplicaciones.

### Inconvenientes de Django
Uno de los principales inconvenientes de Django es que puede ser un poco obstinado, lo que significa que tiene una forma específica de hacer las cosas y puede requerir más instalación y configuración que otros marcos.
También puede tener una curva de aprendizaje empinada para los nuevos usuarios.


## Flask
Flask es un micromarco diseñado para ser liviano y fácil de extender. No viene con muchas funciones listas para usar, pero proporciona un núcleo simple y flexible que permite a los desarrolladores crear sus propias herramientas y bibliotecas sobre él. Algunas de las características clave de Flask incluyen:

### Características claves de Flask
* **Simplicidad**: Flask está diseñado para ser fácil de aprender y usar, con una API mínima e intuitiva. A menudo se usa como una introducción al desarrollo web con Python, ya que requiere menos instalación y configuración que otros marcos.
* **Personalizable**: Flask permite a los desarrolladores elegir las bibliotecas y herramientas que desean usar, en lugar de obligarlos a usar un conjunto específico de herramientas. Esto lo hace altamente personalizable y permite a los desarrolladores crear aplicaciones que se adapten a sus necesidades específicas.
* **Extensibilidad**: Flask está diseñado para ser fácil de ampliar, con una serie de ganchos y puntos de extensión que permiten a los desarrolladores agregar su propia funcionalidad. También tiene un gran ecosistema de extensiones de terceros que brindan características y funcionalidades adicionales.

### Inconvenientes de Flask
Uno de los principales inconvenientes de Flask es que no proporciona tantas funciones para usar como algunos otros marcos, lo que significa que los desarrolladores deberán crear y mantener más de sus propias herramientas y bibliotecas.
También puede requerir más trabajo para configurar y mantener que otros marcos.

## Comparación
A la hora de comparar Django y Flask, no hay una manera fácil, he trabajado con ambos, y hablando en términos generales, la comparación puede volverse inútil, ¿compararás un Ford Ranger con un Ford Mustang? ¿Cuál es mejor?... sí, exactamente, depende de tus necesidades y, potencialmente, de tu estilo y gusto. Tomaré algunos factores clave para ayudar en la decisión.

### Nivel de abstracción
Django es un marco de trabajo de pila completa que proporciona una amplia gama de funciones y abstracciones para facilitar a los desarrolladores la creación de aplicaciones web complejas.

Flask, por otro lado, es un micromarco que proporciona un núcleo mínimo y permite a los desarrolladores construir sus propias funciones sobre él.

Esto significa que Django puede ser una mejor opción para proyectos más grandes y complejos, mientras que Flask puede ser una mejor opción para proyectos más pequeños o para desarrolladores que desean tener más control sobre las herramientas y bibliotecas que utilizan.

### Rendimiento
Ambos usan el estándar WSGI (interfaz de puerta de enlace del servidor web), que les permite implementarse en una variedad de servidores web y entornos de alojamiento. Ambos marcos también tienen soporte de almacenamiento en caché incorporado, lo que puede ayudar a mejorar el rendimiento de las aplicaciones con mucho tráfico o consultas complejas.

Dicho esto, Flask puede tener una ligera ventaja en rendimiento debido a su peso más ligero y diseño minimalista. Debido a que no viene con tantas funciones listas para usar como Django, requiere menos gastos generales y puede manejar las solicitudes de manera más eficiente. Esto es especialmente cierto para proyectos más pequeños o aplicaciones con requisitos más simples, donde las funciones adicionales proporcionadas por Django pueden no ser necesarias.

Vale la pena señalar que la diferencia de rendimiento entre Django y Flask puede no ser significativa en la mayoría de los casos, y otros factores como el hardware y las configuraciones de implementación también tendrán un impacto en el rendimiento general.

### Curva de aprendizaje
En términos de facilidad de uso, Django puede ser más fácil para los nuevos usuarios debido a su conjunto más completo de funciones y abstracciones. Proporciona una amplia gama de herramientas y bibliotecas para manejar tareas comunes de desarrollo web, como el enrutamiento, la representación de plantillas y la interacción con bases de datos. Esto significa que los desarrolladores pueden ponerse en marcha rápidamente y comenzar a crear aplicaciones sin tener que preocuparse por implementar estas funciones desde cero.

Flask, por otro lado, es un micromarco que proporciona un núcleo mínimo y permite a los desarrolladores construir sus propias funciones sobre él. Si bien esto hace que Flask sea altamente personalizable y flexible, es posible que requiera más trabajo de configuración y mantenimiento que Django, ya que los desarrolladores deberán implementar manualmente muchas funciones que otros marcos proporcionan de manera inmediata. Como resultado, Flask puede ser más adecuado para desarrolladores experimentados que se sienten cómodos creando sus propias herramientas y bibliotecas, o que desean tener más control sobre los componentes de su aplicación.

### Nuevas tecnologías
Tanto Django como Flask tienen comunidades sólidas y se desarrollan activamente, lo que significa que es probable que continúen evolucionando y adaptándose a las nuevas tecnologías y tendencias.

No obstante, el diseño ligero y modular de Flask puede facilitar la incorporación de nuevas tecnologías y bibliotecas en una aplicación, ya que los desarrolladores tienen más control sobre los componentes de su aplicación y pueden elegir las herramientas y bibliotecas que mejor se adapten a sus necesidades.

Django, por otro lado, tiene un enfoque más obstinado y puede requerir más instalación y configuración para integrar nuevas tecnologías.

### Popularidad
Ambos marcos son ampliamente utilizados, aquí hay algunos ejemplos.

#### Empresas que usan Django
Django es utilizado por las siguientes empresas gigantes:

* Instagram
* Coursera
*Mozilla
* Pinterest
* National Geographic
* Spotify
*Udemy
* Zapier

#### Empresas que usan Flask
Flask es utilizado por las siguientes compañías gigantes:

* netflix
* Airbnb
* MIT
* Reddit
* Lyft
* Zillow
*Mozilla
* MailGui

## Qué marco elegir
Todo depende de ti, pero no viniste aquí para escuchar eso, ¿verdad? Así que me inspiraré en una historia de viaje para responder a la pregunta.

### Tú eliges Flask
* Empiezas a andar en bicicleta.
* Siendo un novato te equivocas muchas veces.
* Y, te lastimas una y otra vez.
* Ahora, aprendes cosas tu confianza en ti aumenta.

### Tú eliges Django
* Empiezas a andar en bicicleta.
* Pero, hay un giro en la trama.
* Aprendes a andar en bicicleta observando a los demás.
* Te sientas en su espalda y ves lo bien que andan.

## Conclusión
Django y Flask, ambos marcos web son geniales. Django es un framework full-stack con una amplia gama de características y es bueno para proyectos más grandes y complejos. Flask es un micromarco que es liviano y personalizable, lo que lo hace bueno para proyectos más pequeños y desarrolladores que desean más control.

Para concluir, te daré mi opinión personal, basada en las cosas que amo. Como desarrollador de software, aprender cosas nuevas no tiene precio, el error es el otro nombre de la experiencia.

¡Feliz código!


## References
[Quora answer about Flask and Django](https://www.quora.com/Should-I-learn-Flask-or-Django-Im-a-beginner-and-Im-looking-for-simplicity-and-ease-of-learning)

[Flask website](https://flask.palletsprojects.com/)

[Django website](https://docs.djangoproject.com/)

