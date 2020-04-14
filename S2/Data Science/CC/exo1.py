
# coding: utf-8

# In[1]:


"""Extraction d'informations dans un fichier XML"""
################################################################################
# fichier  : exo1.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
from lxml import etree
import json
# Definition locale de fonctions :


# In[3]:


def afficheXML(liste):
    for elem in liste:
        print('*******************************************************************************************************')
        if type(elem) is etree._Element:
            print(etree.tostring(elem,encoding='unicode'))
        else:
            print(elem)


# In[4]:


def xmlTodict(node):
    """
    Renvoie un dictionnaire pour une noeud
    :node: residence node
    :return: dict
    """
    dict_node = {
        'nom': node.xpath("@title")[0],
        'description': node.xpath("@short_desc")[0],
        'latitude': node.xpath("@lat")[0],
        'longitude': node.xpath("@lon")[0],
        'zone': node.xpath("@zone")[0]
    }
    
    return dict_node


# In[5]:


################################################################################
# Corps principal du programme :


# # Exercice 1: Extraction d'informations dans un fichier XML
# Question 1

# In[6]:


tree = etree.parse("rennes-logement.xml")
root = tree.getroot()


# Question 2

# In[7]:


query = "residence[contains(@zone, 'Villejean')]/contact//text()"
print("\n ############# Question 2 #############\n",afficheXML(root.xpath(query)))


# Question 3

# In[8]:


query = "residence[contains(@short_desc, 'Rennes')]"#"[contains(services, 'Local à\xa0 vélos') or contains(services, 'local à\xa0 vélos') or "\
"[contains(services, 'Local à vélos') or contains(services, 'local à vélos')]""[not(contains(services, 'accès sécurisé'))]"

print("\n ############# Question 3 #############\n", afficheXML(root.xpath(query)))


# Question 4

# In[9]:


list_residence = [xmlTodict(residence) for residence in root.xpath("residence")]


# In[10]:


print("\n ############# Question 4 #############\n  Les 4 premiers éléments\n\n", list_residence[:4])


# Question 5

# In[11]:


with open('export_residence.json', 'w', encoding = "UTF-8") as file:
    json.dump(list_residence, file)

