
# coding: utf-8

# In[1]:


"""Script permettant d'explorer les données d'un fichier XML"""
################################################################################
# fichier  : td1.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
from lxml import etree
# Definition locale de fonctions :


# In[3]:


def afficheTexte(listElement):
    for element in listElement:
        print("-----\n")
        for item in element.xpath("child::node()"):
            if item != "\n":
                print(item.text)


# In[4]:


def afficheResultatRequete(listElement):
    for element in listElement:
        if isinstance(element, etree._Element):
            print(etree.tostring(element, encoding='unicode', method='xml'))
        else:
            print(element)


# In[5]:


def infoFilm(listFilm):
    for film in listFilm:
        chaine = ""
        for item in film.xpath("child::node()"):
            if isinstance(item, etree._Element) and item.text:
                if item.getchildren():
                    chaine += "{}: {}\n".format(
                        item.tag, ", ".join([
                            role.text for role in item.xpath("child::ROLE")
                            if role.text
                        ]))
                else:
                    chaine += "{}: {}\n".format(item.tag, item.text)
        print(chaine)


# In[6]:


################################################################################
# Definition des classes :


# In[7]:


################################################################################
# Corps principal du programme :


# # Préambule
# Écrire le code permettant de lire le fichier films.xml et de récupérer l'élément racine de l'arbre XML correspondant. Afficher cet arbre dans la console.

# In[8]:
print("############Préambule############\n")

tree = etree.parse("films.xml")
root = tree.getroot()
print(etree.tostring(root, encoding = "unicode"))


# Écrire le code Python permettant d'obtenir la liste des éléments FILM de l'arbre XML

# In[9]:


listFilm = root.xpath("FILM")


# # EXO 1
# 1. Écrire une fonction `afficheTexte()` permettant d'afficher le contenu textuel d'une liste d'éléments XML passée en paramètre, et de tous leurs sous-éléments. Tester sur la liste des élément FILM obtenue en préambule.

# In[10]:
print("\n############ EXO1.1 ############\nPS: affiche uniquement [2:4]\n")

afficheTexte(listFilm[2:4])


# 2. Écrire une fonction `afficheResultatRequete()` permettant d'afficher le code (XML ou texte) d'une liste d'éléments résultant d’une requête Xpath (cette liste sera passée en paramètre de la fonction).  
# Indication: on pourra tester si les éléments dans cette liste sont des éléments XML en utilisant la fonction `isinstance()` de Python; la classe d’un élément XML dans etree est etree._Element.

# In[11]:
print("\n############ EXO1.2 ############\nPS: affiche uniquement [:3]\n")

afficheResultatRequete(listFilm[:3])


# 3. Écrire une fonction permettant d'afficher les informations d'une liste d'éléments FILM passée en paramètre. Chaque élément FILM sera affiché de la façon suivante (attention, il faudra gérer le cas où le résumé est absent)

# In[12]:
print("\n############ EXO1.3 ############\nPS: affiche uniquement [:3]\n")

infoFilm(listFilm[:3])


# # EXO 2
# Écrire le code Python permettant d'afficher les informations suivantes en utilisant une seule requête **Xpath** (on pourra utiliser la fonction afficheResultatRequete() pour visualiser les résultats lorsque celaest approprié):
# 
# 1. La liste des noms de tous les artistes

# In[13]:
print("\n############ EXO2.1 ############\nPS: affiche uniquement [:5]\n")

query_1 = "ARTISTE/ACTPNOM//text()"
afficheResultatRequete(root.xpath(query_1)[:5])


# 2. Même question mais avec affichage des balises

# In[14]:
print("\n############ EXO2.2 ############\nPS: affiche uniquement [:5]\n")

query_2 = "ARTISTE/ACTPNOM"
afficheResultatRequete(root.xpath(query_2)[:5])


# 3. Afficher le titre des films sortis après 1990

# In[15]:
print("\n############ EXO2.3 ############\nPS: affiche uniquement [:5]\n")

query_3 = "FILM[ANNEE > 1990]/TITRE//text()"
afficheResultatRequete(root.xpath(query_3)[:5])


# 4. Afficher le résumé du film Blade Runner

# In[16]:
print("\n############ EXO2.4 ############\n")

query_4 = "FILM[TITRE = 'Blade Runner']/RESUME//text()"
afficheResultatRequete(root.xpath(query_4))


# 5. Afficher le dernier film du document

# In[17]:
print("\n############ EXO2.5 ############\n")

query_5 = "FILM[last()]"
afficheResultatRequete(root.xpath(query_5))


# 6. Afficher le dernier film du document paru en 1990

# In[18]:
print("\n############ EXO2.6 ############\n")

query_6 = "FILM[ANNEE = 1990 ][last()]"
afficheResultatRequete(root.xpath(query_6))


# 7. Afficher les titres des films qui ont un résumé, puis ceux qui n’en ont pas

# In[19]:
print("\n############ EXO2.7 ############\nPS: affiche uniquement [:5]\n")

query_7 = "FILM[RESUME]/TITRE//text()"
afficheResultatRequete(root.xpath(query_7)[:5])


# 8. Afficher les titres des films vieux de plus de trente ans

# In[20]:
print("\n############ EXO2.8 ############\nPS: affiche uniquement [:5]\n")

query_8 = "FILM[2020 - ANNEE > 30 ]/TITRE//text()"
afficheResultatRequete(root.xpath(query_8)[:5])


# 9. Afficher les titres des films qui contiennent un « V »

# In[21]:
print("\n############ EXO2.9 ############\n")

query_9 = "FILM/TITRE//text()[contains(., 'v') or contains(., 'V')]"
afficheResultatRequete(root.xpath(query_9))


# 10. Afficher les titres des films dont le texte du résumé contient le mot "amour"

# In[22]:
print("\n############ EXO2.10 ############\n")

query_10 = "FILM[RESUME[contains(., 'amour')]]/TITRE//text()"
afficheResultatRequete(root.xpath(query_10))


# 11. Afficher le nombre de films

# In[23]:
print("\n############ EXO2.11 ############\n")

query_11 = "count(FILM)"
print(root.xpath(query_11))


# 12. Afficher le nombre de drames

# In[24]:
print("\n############ EXO2.12 ############\n")

query_12 = "count(FILM[GENRE = 'Drame'])"
print(root.xpath(query_12))


# 13. Donner les noms des acteurs qui ont joué dans Vertigo

# In[ ]:




