import os
import unicodedata
from xml.dom import minidom


def elimina_tildes(cadena): #Función para quitar las tildes de los nombres. Utiliza el modulo "unicodedata".
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s
def segundoprograma(path,path_txt,path_txt_modif,path_txt_nombres): #Función para crear un fichero por sesión con los nombres de los hablantes + parrafos en los que intervienen.
    with os.scandir(path) as entries: #Creamos una lista con todos los ficheros .xml ubicados en la dirección "path".
        
        for entry in entries:
            print("TRABAJANDO EL SIGUENTE FICHERO: ",entry.name)
            mydoc = minidom.parse(path+entry.name) 
            turns = mydoc.getElementsByTagName("turn")

            for elem in turns:
                
                ## Primero creamos un fichero con todos los parrafos del .xml.
                with open(path_txt+entry.name.strip("_transcription.xml")+".txt", 'a', encoding="utf-8") as f:  # Direccion donde crearemos los primeros archivos .txt + el nombre antiguo.TXT !!!                 
                    nombres= elem.attributes['speakerId'].value
                    f.write("{} {}".format('*'+nombres, elem.firstChild.data))  #Esto escribe todo lo que esté entre <turn> y <\turn>
                       

    with os.scandir(path_txt) as entries: #Creamos una lista con todos los ficheros .txt ubicados en la dirección "path_txt".


        for entry in entries:          
            izenak=[]
            izenak_ordenatu=[]
            parrafo_zenbakiak=[]
            with open(path_txt+entry.name, 'r', encoding="utf-8") as g: #Abrimos las sucesivas carpetas del directorio seleccionado.
                j=1
                for linea in g.readlines():
                    if linea[0]=="*":
                        a= linea.strip("*") #Borramos el indicador del comienzo. 
                        a= a.strip('\n') #Borramos el salto de pagina que tienen los nombres.
                        a= elimina_tildes(a)
                        izenak_ordenatu.append(a)
                    else:                             
                        izenak.append(a)
                        parrafo_zenbakiak.append(j)
                        j+=1
            
            izenak_ordenatu=sorted(set(izenak)) #set() para borrar elementos repetidos y sorted() para ordenalos alfabeticamente. 

            for i in range(len(izenak_ordenatu)): #Carpetas por sesión.
                with open(path_txt_modif+entry.name, 'a', encoding="utf-8") as o:
                            o.write("%s\n"%(izenak_ordenatu[i]))
                for r in range(len(izenak)):
                    if izenak[r]==izenak_ordenatu[i]:               
                        with open(path_txt_modif+entry.name, 'a', encoding="utf-8") as o:
                            o.write("%i\n"%(parrafo_zenbakiak[r]))
            
            for i in range(len(izenak_ordenatu)):
                with open(path_txt_nombres+izenak_ordenatu[i]+".txt", 'a', encoding="utf-8") as o: # Carpetas por Nombre.
                            o.write("\t%s\n"%("SESION:"+entry.name.strip(".txt")))
                for r in range(len(izenak)):
                    if izenak[r]==izenak_ordenatu[i]:               
                        with open(path_txt_nombres+izenak_ordenatu[i]+".txt", 'a', encoding="utf-8") as o:
                            o.write("%i\r"%(parrafo_zenbakiak[r]))
            
                                  
        

                        

#================= PROGRAMA PRINCIPAL =================#

#IMPORTANTE: CADA VEZ QUE SE EJECUTA EL PROGRAMA LIMPIAR LOS DIRECTORIOS "path_txt" Y "path_txt_modif"

path='C:/Users/Joseba/Desktop/Joseba/2.tarea/BPdb/BPdbLong/transcriptions/' # Directorio donde se encuentran los archivos ".xml".
path_txt= 'C:/Users/Joseba/Desktop/Joseba/2.tarea/BPdb/BPdbLong/programa2_txt_1/' #Direcotorio para mandar los archivos ".xml" convertidos a "txt"
path_txt_modif= 'C:/Users/Joseba/Desktop/Joseba/2.tarea/BPdb/BPdbLong/programa2_txt_2/' #Directorio para mandar nombres+parrafos por cada sesión en fmt ".txt"  
path_txt_nombres= 'C:/Users/Joseba/Desktop/Joseba/2.tarea/BPdb/BPdbLong/nombres/' #Directorio para mandar sesiones+parrafos por cada hablante en fmt ".txt"  

segundoprograma(path,path_txt,path_txt_modif,path_txt_nombres)



