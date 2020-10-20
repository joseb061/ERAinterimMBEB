import os
from xml.dom import minidom


def primerprograma(path,path_txt,path_txt_modif):
    with os.scandir(path) as entries: #Creamos una lista con todos los ficheros .xml ubicados en la dirección "path"
        
        for entry in entries:
            print("TRABAJANDO EL SIGUENTE FICHERO: ",entry.name)
            mydoc = minidom.parse(path+entry.name) 
            turns = mydoc.getElementsByTagName("turn")

            for elem in turns:
                
                ##Primero creamos un fichero con todos los parrafos del .xml
                with open(path_txt+entry.name.strip("_transcription.xml")+".txt", 'a', encoding="utf-8") as f:  # Dirección donde crearemos los primeros archivos .txt + el nombre antiguo.TXT !!!                 
                    f.write(elem.firstChild.data)  #Escribit todo lo que esté entre <turn> y <\turn>
            
                ## Una vez que tenemos los ficheros con toda la información borramos todos los espacios en blanco y etiquetamos cada parrafo con su correspondiente numero. 
            with open(path_txt+entry.name.strip("_transcription.xml")+".txt", 'r', encoding="utf-8") as infile, open(path_txt_modif+entry.name.strip("_transcription.xml")+".txt", 'a',encoding="utf-8",newline='') as outfile:
                j=1
                for line in infile:
                    if not line.strip():  continue  # Salto de la linea en blanco.
                    outfile.write("{} {}".format(j, line))
                    j+=1 # Número del parrafo.



#================= PROGRAMA PRINCIPAL =================#

path='' # Directorio donde se encuentran los archivos ".xml".
path_txt= '' #Direcotorio para mandar los archivos ".xml" convertidos a "txt"
path_txt_modif= '' #Directorio para mandar parrafos enumerados por cada sesión en fmt ".txt" 

primerprograma(path,path_txt,path_txt_modif)
