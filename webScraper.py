import requests
import os
from bs4 import BeautifulSoup
import shutil

naic_links_path = "output_of_webscraper/naic_links.txt"
rejected_naic_links_path = "output_of_webscraper/rejected_naic_links.txt"
results_textfile = [naic_links_path, rejected_naic_links_path]
destination_folder = "/share/s3453g1/keysha/Development/AO_web_research/webscraper/output_of_webscraper"
other_links_path = "/share/s3453g1/keysha/Development/AO_web_research/webscraper/output_of_webscraper/other_links.txt"

info = []

# Se define una función llamada main().
def main():
    # Al comienzo de la función, se utiliza la función open() para abrir un archivo llamado "naic_links.txt" en modo de escritura ("w"), Sin embargo, no se asigna el objeto de archivo devuelto a ninguna variable.
    open(naic_links_path, "w")
    open(rejected_naic_links_path, "w")
    open(other_links_path, "w")
    global rejected_naic_links 
    rejected_naic_links = set()
    
    
    # se asigna la URL "https://www.naic.edu/ao/landing" a la variable URL.
    URL = "https://www.naic.edu/ao/landing"  #starting value

# listado adentro de otro listado
    working_list = [["start",URL]]  #defining starting value
    finished_list =[]
    final_naic_links = set()
    final_other_links  = set()
    i = 0
    # cuando corra que termine en 3 millones y se acaba la corrida
    # Se inicia un bucle while que se ejecutará siempre que la longitud de working_list sea mayor que 0. Si el valor de i supera los 3000000, el programa se detiene mediante la función quit().
    while len(working_list) > 0: 


         # current_url selects URL from working list and source_url selects "start" from working_list. working_list.pop deletes workinglist
        #Se obtiene la URL actual y la URL de origen de la lista working_list, que se encuentran en la posición [0][1] y [0][0], respectivamente. Luego, se elimina el primer elemento de working_list utilizando el método pop(0).
        global current_url 
        current_url = working_list[0][1]
        # Verifica si current_url tiene \n, si lo tiene, borra todos los que hayan
        current_url = current_url.replace("\n","")
        current_url = current_url.replace(" ", "")
        # Lo mismo con 

        global source_url 
        source_url = working_list[0][0]
        working_list.pop(0)

        # cuando se corre brinca lo que se le indico
        # Se realiza una serie de comprobaciones condicionales para verificar si la current_url ya está en finished_list o si termina con una extensión de archivo específica. Si se cumple alguna de estas condiciones, se agrega current_url a finished_list y se utiliza la instrucción continue para pasar a la siguiente iteración del bucle.
        if current_url in finished_list:
            continue
        continue_loop = False
        if current_url.endswith("mp4"):
            
            continue_loop = True
        elif current_url.endswith("pdf"):
            
            continue_loop = True
        elif current_url.endswith("png"):
            
            continue_loop = True
        elif current_url.endswith("jpg"):
            
            continue_loop = True
        elif current_url.endswith("JPG"):
           
            continue_loop = True
        elif current_url.endswith("gif"):
           
            continue_loop = True
        elif current_url.endswith("ps"):
           
            continue_loop = True
        elif current_url.endswith("eml"):
           
            continue_loop = True
        #Se realizan más comprobaciones condicionales para verificar si current_url contiene ciertas subcadenas específicas. Si se cumple alguna de estas condiciones, se agrega current_url a finished_list y se utiliza la instrucción continue para pasar a la siguiente iteración del bucle.
        if "www.naic.edu/datacatalog" in current_url:
            continue_loop = True
        elif "www.naic.edu/aoweb_images" in current_url:
            continue_loop = True
        
        if continue_loop == True:
            finished_list.append(current_url)

        if continue_loop == True:
            set_length = len(rejected_naic_links)
            rejected_naic_links.add(current_url)
            set_length_2 = len(rejected_naic_links)

            if set_length_2 != set_length:
                with open(rejected_naic_links_path, "a") as rejected_file:
                    rejected_file.write(source_url + "\t" + current_url + "\n")
            continue
        continue_loop = False
        # hacerle breakpoint depues que encuentre ese string para saber como hacer qe no lo repita
        # if "http://www.naic.edu/%7Ephil/hardware/12meter/patriot12meter.html" in current_url:
        #     breakpoint()
        # unique_links, naic_links, other_links = extract_links(current_url)
        try:
            unique_links, naic_links, other_links = extract_links(current_url)
        except:
            # print(current_url)
            
            finished_list.append(current_url)
            continue


        print(current_url)
        with open(naic_links_path, "a") as naic_results_file:
            naic_results_file.write(source_url + "\t" + current_url + "\n")
            i+=1

        with open(other_links_path, "a") as other_file:
            for href in other_links:
                if href not in final_other_links:
                    other_file.write(source_url + "\t" + href +"\n")
                    final_other_links.add(href)


        # with open(rejected_naic_links_path, "a") as rejected_file:
        #     for link in rejected_naic_links:
        #         rejected_file.write(source_url + "\t" + current_url + "\n")
            

        naic_links = list(naic_links)

        # Add url to finished
        finished_list.append(current_url)
        
        
        naic_links_filtered = []
        for link in naic_links:
            if link not in finished_list:
                naic_links_filtered.append(link)
            
                        
        for link in naic_links_filtered:
            working_list.append([current_url, link])
    

    # with open("naic_href_links.txt", "w") as naic_file:
    #     for href in finished_list:
    #         naic_file.write(href + "\n")



    # # Print all NAIC links one by one
    # for link in naic_links:

    #     unique_links, nested_naic_links, nested_other_links = extract_links(link)
    #     # run function through each link

    # print(link)

    # with open("naic_href_links.txt", "w") as naic_file:
    #     for href in naic_links:
    #         naic_file.write(href + "\n")

    # with open(other_links_path, "a") as other_file:
    #     for href in other_links:
    #         other_file.write(source_url + "\t" + current_url +"\n")

                                                 

def extract_links(URL):
    # Send a GET request to the website
    # agarra url con request y se guarda adentro de response.
    response = requests.get(URL)

    # Parse (analiza el) the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all <a> tags and extract href attributes
    links = soup.find_all("a")

    # Extract href attributes
    # set() es como un listado y es para que no repita
    # hace un set que no tiene nada adentro
    unique_links = set()
    for link in links:
        href = link.get("href") #El href se extrae utilizando .get(), se chekea si no es null y se agrega a unique_links.
        if href:
            unique_links.add(href)
    naic_links = set()
    other_links = set()
# que coja los href del www.naic.edu y lo separe en dos dif listado.todas las cosas de naic lo envia a naic_links y lo que sobre que no tenga nada de naic lo envia a other_links.
    for link in links:
        href = link.get("href")
        if href:
            if "www.naic.edu" in href:
                    
                naic_links.add(href)
            else:
                other_links.add(href)
#La función devuelve una tupla que contiene los conjuntos unique_links, naic_links y other_links. Estos conjuntos contienen los enlaces extraídos y clasificados según si pertenecen al dominio "www.naic.edu" o no.
    return unique_links, naic_links, other_links  
 


if __name__ == "__main__":
    main()