Para poder procesar los archivos XML-s procedentes de las actas usamos dos programas python: &quot;programa1.py&quot; y &quot;programa2.py&quot;.

**PRIMER PROGRAMA**

El primer programa está compuesto por una función y un programa principal. Este ultimo toma como variables tres directorios diferentes. Por un lado el directorio _input_:

- &quot;Path&quot;= dirección de la carpeta en la que residen todos los archivos XML.

Y por otro lado los dos directorios _output_:

- Path\_txt= dirección de la carpeta en la que se depositarán todos los párrafos de los archivos XML en formato &quot;.txt&quot; (un fichero &quot;.txt&quot; por cada fichero &quot;.xml&quot;).
- Path\_txt\_modif= dirección de la carpeta en la que se depositaran los párrafos de cada sesión enumerados desde el numero 1 al número &quot;n&quot; (un fichero &quot;.txt&quot; por cada fichero &quot;.xml&quot;).

\*Una vez que se ejecuta el programa, este genera una serie de ficheros. En el caso de volverlo a ejecutar con las mismas direcciones de salida, borrar los ficheros antiguos.

**SEGUNDO PROGRAMA**

El segundo programa, al igual que el primero, está compuesto por una función y un programa principal. Este ultimo toma como variables cuatro directorios diferentes. Por un lado el directorio _input_:

- &quot;Path&quot;= dirección de la carpeta en la que residen todos los archivos XML.

Y por otro lado los dos directorios _output_:

- &quot;Path\_txt&quot; = dirección de la carpeta en la que se depositarán todos los nombres de los hablantes con sus respectivos discursos en formato &quot;.txt&quot; (un fichero &quot;.txt&quot; por cada fichero &quot;.xml&quot;).
- &quot;Path\_txt\_modif&quot; = dirección de la carpeta en la que se depositaran los nombres de cada hablante junto con los números de los párrafos en los que hablan por cada sesión.
- &quot;Path\_txt\_nombres&quot; = dirección de la carpeta en la que se depositaran el número de los párrafos por sesión en los que ha hablado cada hablante (un fichero &quot;.txt&quot; por cada persona).

\*Una vez que se ejecuta el programa, este genera una serie de ficheros. En el caso de volverlo a ejecutar con las mismas direcciones de salida, borrar los ficheros antiguos.