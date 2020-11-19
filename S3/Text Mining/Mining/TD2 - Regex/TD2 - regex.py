# coding: utf-8

__author__: "Loic Rakotoson"

# Utilisation des expressions régulières
# --

# In[1]:


import re


# ## 1. Extraction d'URL
# À partir du fichier `extrait.html` fourni, écrire un programme Python qui extrait dans un nouveau fichier texte, la liste de tous les liens de la page HTML ainsi que le texte du lien associé à chaque URL.

# In[2]:


with open("data/extrait.html", encoding="utf-8") as r, open("data/links.txt", 'w', encoding='utf-8') as w:
    for line in r.readlines():
        link = re.findall(r'<a\s*(href=.+)>\s*(.+)\s*</a>', line, re.I)
        if len(link):
            link = link[0]
            w.write(f'{link[0][6:-1]} = {link[1].strip()}\n')
            print(f'{link[0][6:-1]} = {link[1].strip()}')


# ## 2. Traitement d'emails
# Écrire un programme Python qui permet à l'utilisateur de saisir une adresse e-mail et extrait et affiche à partir de cette adresse les 4 éléments suivants:  
# - nom
# - prénom *(facultatif)*
# - serveur
# - domaine

# In[3]:


with open("data/td3_exo2_adressesMail.txt") as f:
    for line in f.readlines():
        parse = re.findall(r"([\w-]+)\.*([\w-]+)*@(.+)\.(.{2,3})", line)[0]
        print(
            f"{line}> {dict(zip(['nom','prenom','serveur','domaine'], parse))}"
        )


# ## 3. Traitement de logs
# Extraire depuis `log.txt` vers `log_out`, pour une ouverture se session, le nom, la date et l'heure.  
# `Jul 26 20:06:34  PAM_unix[15771]: (system-auth) session opened for user brejeon by (uid=0)` $\to$ `brejeon: Jul 26 (20h06)`

# In[4]:


with open("data/log.txt") as r, open("data/log_out", 'w') as w:
    for line in r.readlines():
        parse = re.findall("([a-zA-Z]{3})\s+(\d{1,2}) (\d{2}:\d{2}).*?opened for user (\w+) by.*", line)
        if len(parse):
            parse = parse[0]
            print(f"{parse[3]}: {parse[0]} {parse[1]} ({parse[2].replace(':','h')})", file=w)


# ## 4. Nettoyage de page HTML
# ### Question 1:
# Écrire un programme Python qui procède au nettoyage complet du document `Sigles.txt` (suppression de tous les éléments liés au langage HTML ou autres codages Web, élimination des lignes vides, etc.) et récupère dans un nouveau fichier le texte brut.
# ### Question 2:
# Modifier votre programme pour qu'il puisse extraire également dans un nouveau fichier texte nommé `liste_sigles` toutes les abréviations (en majuscule) qui sont contenues dans ce document.

# In[5]:


htag = re.compile("<\/?[\w\s]*>|<.+[\W]>|[\n\t\ufeff]+")
with open("data/Sigles.txt", encoding = "utf-8") as f:
    file = re.sub('\s+', ' ', htag.sub(' ', f.read())).strip()


# In[6]:


with open("data/liste_sigles", 'w') as f:
    print(*set(re.findall('([A-Z]{2,})[\s+|\.$]', file)), sep = '\n', file = f)

