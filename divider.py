


 
naic_links_path = "output_of_webscraper/naic_links.txt"
list_terminada = []
divider_naic_links = set()
link_set = set()
asking_number = input("please type number on the level you want")
asking_number = int(asking_number)
with open(naic_links_path, 'r') as file:
    for line in file:
        
        naic_tab_split = line.strip().split('\t')
        link = naic_tab_split[1]
        link_split = link.split("/")
        link_sliced = link_split[2:]
        link_sliced_backwards = link_sliced[:asking_number]
        rejoin_slash = "/".join(link_sliced_backwards)
        link_set.add(rejoin_slash)
        

    for link in link_set:
        print(link)
    
    
         
        