Para poder procesar los archivos XML-s procedentes de las actas usamos dos programas python: “programa1.py” y “programa2.py”. 

PRIMER PROGRAMA

El primer programa está compuesto por una función y un programa principal.  Este ultimo toma como variables tres directorios diferentes. Por un lado el directorio input: 

•	“Path”= dirección de la carpeta en la que residen todos los archivos XML.

Y por otro lado los dos directorios output:

•	Path_txt= dirección de la carpeta en la que se depositarán todos los párrafos de los archivos XML en formato “.txt” (un fichero “.txt” por cada fichero “.xml”).
•	Path_txt_modif= dirección de la carpeta en la que se depositaran los párrafos de cada sesión enumerados desde el numero 1 al número “n” (un fichero “.txt” por cada fichero “.xml”). 

*Una vez que se ejecuta el programa, este genera una serie de ficheros. En el caso de volverlo a ejecutar con las mismas direcciones de salida, borrar los ficheros antiguos.

   SEGUNDO PROGRAMA

El segundo programa, al igual que el primero,  está compuesto por una función y un programa principal.  Este ultimo toma como variables cuatro directorios diferentes. Por un lado el directorio input: 

•	“Path”= dirección de la carpeta en la que residen todos los archivos XML.

Y por otro lado los dos directorios output:

•	“Path_txt” = dirección de la carpeta en la que se depositarán todos los nombres de los hablantes con sus respectivos discursos  en formato “.txt” (un fichero “.txt” por cada fichero “.xml”).
•	“Path_txt_modif” = dirección de la carpeta en la que se depositaran los nombres de cada hablante junto con los números de los párrafos en los que hablan por cada sesión.
•	“Path_txt_nombres” = dirección de la carpeta en la que se depositaran el número de los párrafos por sesión en los que ha hablado cada hablante (un fichero “.txt” por cada persona).

*Una vez que se ejecuta el programa, este genera una serie de ficheros. En el caso de volverlo a ejecutar con las mismas direcciones de salida, borrar los ficheros antiguos.
