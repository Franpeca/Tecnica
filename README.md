# Prueba técnica

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)


## 📝 Descripción

Este repositorio corresponde a la prueba técnica para acceder a las prácticas de empresa.  
Se busca integrar una serie de herramientas del ámbito de la arquitectura e ingeniería de datos. Desde la generación de los mismos como su tratamiento e incorporación en bases de datos, usando para ello software actual y profesional y que pueda ser usado en producción.

Las herramientas principales utilizadas han sido:

* Docker: Para la construcción de los contenedores y portabilidad del código en diferentes plataformas.
* Kedro: Orquestador a nivel de procesamiento de datos para la generación y tratamiento de estos.
* PostgreSQL: Como base de datos principal para Airflow y para los datos.
* Airflow: Orquestador superior que permite la realización de las diferentes tareas a pedir.


## 🎯 Objetivos

**✔️ Se ha logrado implementar todo lo pedido en el guión de la prueba.**  

Los **objetivos del proyecto** y que se han logrado alcanzar son:

* Generación de datos
* Limpieza de datos
* Carga en base de datos
* Orquestación de tareas
* Contenerización

Y como otros **objetivos opcionales** que se han alcanzado son:

* Uso de frameworks de ingeniería de datos y pipelines de datos

**Durante el desarrollo**, se tuvo también como objetivo aspectos como:

* Correcta funcionalidad de lo que se pedía en el guión de prácticas.
* Código limpio y documentado.
* Código modular, teniendo presente la separación de tareas a nivel de código.
* Asignación correcta de orquestación, tanto para Airflow como Kedro, buscando la separación de tareas a nivel de tareas.
* Escalabilidad y flexibilidad en todo el proyecto. Tanto a nivel tareas generales como procesos concretos de datos.
    * Capacidad para poder incorporar en un futuro nuevas pipelines de procesamiento de datos de forma fácil y flexible, sin afectar al resto de DAGs.
    * Capacidad de agregar nuevas herramientas en entornos aislados que permitan interactuar con el resto de aplicaciones existentes.
* Control de errores y documentación de lo que se está realizando en cada proceso.
* Uso de repositorios y control de versiones. Documentación constante de los cambios.
* Seguimiento de **buenas prácticas** en diversas partes del proyecto, tanto en la forma de codificar como en la lógica seguida en los scripts de python, docker-compose.yml, entre otros.

## 🛠️ Cómo instalar y lanzar el proyecto


> ⚠️ Se podría haber realizado un script para automatizar muchas de estas partes, pero me he ceñido al documento y a lo que entendido en las reuniones. Es por esto que *"lanzar todo con un click"* lo entiendo como que todo se levante con *docker-compose* y que es lo que se pretendía. Ha sido una decisión de diseño, no por falta de tiempo.


### 🐧 Linux
Se requiere tener instalado previamente:
* Git
* Docker y Docker Compose


##### 1. Clonacion del repositorio
```
git clone https://github.com/Franpeca/Tecnica.git
```
##### 2. Lanzamiento de Docker

> ⚠️ Es necesario ser tener permisos root **solo para los siguientes dos comandos**.

Se debe de asegurar que se está lanzando Docker. Se puede comprobar con:
```
sudo systemctl status docker
```
Si no se encuentra lanzado, se puede lanzar de la siguiente forma (se supone que se tiene acceso root):
```
sudo systemctl start docker
```

##### 3. Lanzamiento de los contenedores con Docker-compose
Realizar el siguiente comando para acceder al directorio del repositorio:
```
cd Tecnica/
```
Ejecutar el siguiente comando para levantar los contenedores. 

> ⚠️ La primera vez que se ejecute tardará bastante dado que hay que descargar todas las imágenes. 
```
docker-compose up -d
```
Tras esto, se lanzarán todos los contenedores con su configuración correspondiente.
Se pueden listar los contenedores existentes con:
```
docker ps
```

Para bajar los contenedores (manteniendo volúmenes y redes), hay que ejecutar el siguiente comando:
```
docker-compose stop
```
##### 4. Acceso a Airflow
En la web siguiente se podrá acceder al contenido de Airflow.
```
localhost:8080
```
Los credenciales de inicio de sesión de Airflow son:
  * Usuario: admin
  * Contraseña: admin

En caso de acceder a cualquiera de los contenedores por terminal, la contraseña por defecto es:
* admin

### 📂 Windows
Se puede realizar a través de alguno de los siguientes programas:
* Docker Desktop
* Docker Toolbox

La clonación del repositorio se puede realizar a través del programa *Git* tanto por terminal como por gráfico. O también se puede descargar un comprimido del repositorio y extraerlo en donde se desee.

El acceso a Airflow y los credenciales son los mismos que los expuestos en el apartado de *Linux*


## 📌  Notas sobre el desarrollo

Decir que se han usado asistentes virtuales como *ChatGPT*, *DeepSeek* y *Github Copilot* tal y como se aconsejó en las reuniones. Esto ha ayudando muchísimo en el entendimiento y desarrollo del proyecto. También tenía presente lograr resultados correctos usando estas tecnologías. 

Antes de ponerme manos a la obra, pensé en cómo tendría que estructurar todo e investigué bien cómo funcionaban los contenedores a nivel de lógica, si podía comunicarme entre ellos como quisiera o si habian algunas restricciones. Tras esto, pensé en incorporar Kedro de forma aislada primero y cuando tuviera ya los datos montar la base de datos. Después, empecé a usar Docker para montar las cosas que yo mismo creé. Es decir, primero creé una base con la que empezar a trabajar y cuando ya tenía cosas mías, las pasé a Docker, ya que no iba a usar Docker sin tener nada que montar. Una vez me funcionaba todo por separado y en su respectivo contenedor, decidí montar Airflow y trabajé en la comunicación entre contenedores. Una vez funcionaba, pasé a elaborar los DAGs sabiendo que podía acceder sin problema.

Podría hablar mucho más sobre varios detalles, pero intentaré comentar lo más relevante de cada parte:

#### *Kedro*
*Kedro* se utiliza para proyectos de ciencias de datos, gestionando las *pipelines* de procesos relacionados con esto. En esta parte (en sus carpetas) se encuentra el código que genera y limpia los datos.

La motivación de usar *Kedro* en esta prueba es reflejar una buena práctica tanto en cómo se desarrollan estos procesos como en la organización del código, además de dar características como modularidad, separación de tareas, reutilización, etc., en el nivel de procesamiento de datos. 

Con *Kedro* se podrían integrar fácilmente otras tareas de tratamiento de datos, por ejemplo, para nuestro caso se podrían realizar diferentes formas de limpiar los datos o diferentes fuentes de generación, simulando un entorno real donde se obtienen *volúmenes* de datos. También permitiría realizar pruebas directamente y de forma modular. **Desde el inicio de la prueba, se ha tenido esta idea en mente, desarrollando todo en base a ello.**

En relación a los *scripts* de datos, no hubo mucha complicación en su realización. Gran parte se realizó de forma directa gracias a los asistentes virtuales y al conocimiento típico del tratamiento de *datasets*.

El problema principal con *Kedro* fue cómo manejar los *volúmenes* para que se sincronizaran correctamente los cambios, además de problemas de permisos relacionados con la generación de su imagen. Pero esto se logró solventar modificando el *Dockerfile* y el *docker-compose.yml*. También en la construccion de su imagen, ya que fue aquí donde entendi finalmente por completo cómo funcionaban los volúmenes de Docker.


#### *PostgreSQL*
En él se crean dos bases de datos, *airflow_db* y *data_db*. En la primera se encuentran elementos de *Airflow* y en la segunda es donde se volcarán los datos. En el *docker-compose.yml* se puede observar cómo se han realizado la creación de las tablas y de los usuarios.

Entre las características principales se puede ver que, al levantar el contenedor, se realizan comprobaciones de que existan las bases de datos anteriormente y, en caso negativo, las crea, **para así no machacar lo que ya existe cada vez que se levanten los contenedores**. Los datos de la base de datos **persisten aunque se bajen los contenedores**.

A la hora de insertar los datos, se realizan comprobaciones en los *DAGs*, para que en caso de que un *item* exista en la base de datos, se pueda no introducir este y continuar introduciendo el resto.

El tema de la conexión con la base de datos fue el mayor problema, posiblemente el que retrasó más el proyecto. Esto es debido a que no podía conectarme a la base de datos, intentaba dejar por defecto unas credenciales de conexión, pero no se quedaban guardadas. Entonces, a raíz de esto, vi que era a causa de problemas con los permisos, por lo que tuve que cambiar muchas partes y volver a probar todo.  


#### *Airflow*
Se han creado 4 ***DAGs***:
* 01: Comprobación de contenedores y de datos existentes.
* 02: Generar los datos con *Kedro* usando *kedro run.*
* 03: Inserción de los datos en la base de datos.
* 04: Borrado completo de los datos en la base de datos *(extra, para pruebas y visualización de funcionamiento de partes)*.

Como se ha dicho ya, se buscaba separar funcionalidades y la parte de los datos los genera *Kedro*. La parte de volcado, al ser más general, se ha decidido que se realice a través de un *DAG*, ya que esta tarea no corresponde a un flujo de datos como se realiza en *Kedro*. Además, así se demuestra un mayor conocimiento de los *DAGs*. También, se han añadido funciones de control de errores para saber qué ha estado fallando, revisando para ello los *logs* en la web (aquí la decisión de documentar bien las salidas en la parte de *Kedro*, entre otros).

En relación a los problemas, el mayor nuevamente ha sido los permisos. **Soy consciente de que es una mala práctica** que el usuario *root* sea el usuario por defecto de este contenedor, pero nuevamente, tuve mucho problema con los permisos. Puedo lograr que *Airflow* tenga su usuario por defecto, pero cuando lo logro, obtengo problemas con el grupo *Docker* y se me presentan problemas al acceder al *socket*, impidiéndome la comunicación entre contenedores e incluso la ejecución. Creo que el problema es cómo creo estos usuarios en el *docker-compose* e incluso en cómo se registra la información de *Airflow* en la base de datos.

#### *Docker*
Hay varios contenedores de *Docker*, indicados en el fichero *docker-compose.yml*. Se ha decidido incorporar también *Kedro* en un entorno propio ya que este tipo de *framework* se utiliza en áreas con muchas librerías pesadas, como *Scikit-Learn* o *PyTorch*, entre otras. El levantamiento de todos los contenedores se logra únicamente con *docker-compose.yml*, ahí se puede ver reflejado cómo se han montado los volúmenes, buscando todo el rato una correcta forma de tratarlos. **Tenía claras dos cosas desde el inicio del desarrollo**, una era que el contenido de *Kedro* se sincronizara entre el contenedor y el repositorio local y la otra que el contenido de la base de datos no se perdiera tras cerrar los contenedores. Hasta donde me ha permitido el tiempo, esto se cumple.
Se ha creado una imagen de Kedro propia ya que este no dispone de una imagen en Docker Hub, por lo que se ha creado un *Dockerfile* para ello. **No es necesario construir la imagen**, mi imagen está subida a *Docker Hub* y se descarga de forma automática la primera vez que se lanzan los contenedores en una máquina nueva.

Nuevamente, el tema de los permisos ha sido un problema, y es a raíz de este fichero. También, sé que hay partes que quizá podrían estar un poco mejor hechas en esta parte, pero que tuve que dejar así dado que me estaba retrasando demasiado y no había avanzado en otras.

Otro problema relacionado con *Docker* y por el cual perdí un día entero fue por el tema de la virtualización. *Docker* utiliza en *Windows* una virtualización llamada *Hyper-V* junto con el subsistema de *Linux* para *Windows*, en concreto el 2, y ambas de estas tecnologías **no funcionan en mi ordenador personal ni en un portátil que me prestaron**. Tuve que crear una máquina virtual de *Linux* y ahí pude realizar todo. Para probar el proyecto en *Windows* probé a crear una máquina virtual, pero tras instalar *Docker* en ella no me dejaba iniciar *Windows*. El problema era nuevamente por *Hyper-V*. Es por esto que **no he podido probar al completo el proyecto en un entorno *Windows***.

He intentado tener cuidado con cómo atribuyo permisos y usado scripts de *bash*, para que se ejecuten en los contenedores y que así no haya problema con *Windows*, pero aun así las rutas de los volúmenes están en formato *Linux* y no dinámicas, dado que no he podido probar. Aun así, hasta donde leí en la documentación, *Docker Desktop* se encarga de esto último.


## 💡  Cosas que quería implementar

Dada la falta de tiempo, sobre todo perdido por problemas relacionados con mi *hardware* y problemas con los permisos, no he podido realizar muchas de las cosas que me gustaría.  En los objetivos comento ideas que tenía en mente durante el desarrollo. Preferí priorizar estas ya que considero que son muy importantes, pero por tiempo se quedaron fuera otras.

❌ La lista principal de cosas que no se han podido implementar es:

* Añadir nodos en Kedro (funciones) para mostrar un mejor uso de Kedro y de sus pipelines.
* Integración de pruebas unitarias en Kedro, permitiendo mejorar el tratamiento de los datos y de futuras ampliaciones.
* Mejor uso de los permisos, en concreto, del contenedor de Airflow.
* Uso de restricciones y triggers de auditoría, seguridad, dominio, integridad y extensión en la base de datos.
* DAGs adicionales, en concreto para los nuevos procesos de Kedro.
* Dependencias entre DAGs y mostrar el potencial de uso de Airflow teniendo varios DAGs.
* Herramienta personalizada para visualizar los datos en navegador, formato dashboard.
* Capa de seguridad de cara al manejo de contraseñas y cómo quedan reflejadas en el *docker-compose.yml*.
* Pruebas unitarias para cada parte, para demostrar el correcto funcionamiento de forma rápida.
* Diagrama profesional con el funcionamiento del proyecto. Diviendo sus partes y mostrando como se comunica todo.

Muchas de estas partes son relativamente fáciles de añadir, ya que se planeó todo teniendo esto en mente.  
Otras, como las herramientas, podrían haber sido un poco más difíciles de implementar. Aun así, creo que a pesar de los imprevistos, he logrado realizar lo esencial, intentando seguir buenos métodos y aprendiendo cómo funciona cada componente.
