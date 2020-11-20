# coding: utf-8

"""
Le Chatbot français avec qui tu peux parler de ta journée
"""

__author__: "Lrakotoson"

# In[1]:


from nltk.chat.util import Chat
from datetime import datetime


# In[2]:

# ascii art en ligne de commande
art = """
           ,,                          ,,                          
         `7MM                   mm    *MM                    mm    
           MM                   MM     MM                    MM    
 ,p6"bo    MMpMMMb.   ,6"Yb.  mmMMmm   MM,dMMb.   ,pW"Wq.  mmMMmm  
6M'  OO    MM    MM  8)   MM    MM     MM    `Mb 6W'   `Wb   MM    
8M         MM    MM   ,pm9MM    MM     MM     M8 8M     M8   MM    
YM.    ,   MM    MM  8M   MM    MM     MM.   ,M9 YA.   ,A9   MM    
 YMbmd'  .JMML  JMML.`Moo9^Yo.  `Mbmo  P^YbmdP'   `Ybmd9'    `Mbmo 
"""


# In[3]:

# dictionnaire de traduction personne-machine
reflect = {
    "je suis": "tu es",
    "j'ai": "tu as",
    "j'": "tu",
    "je serai": "tu seras",
    "je": "tu",
    "mon": "ton",
    "ma": "ta",
    "moi": "toi",
    "notre": "votre"
}

reflect.update({v:k for k,v in reflect.items()})


# In[4]:

# Règles
pairs = [
    (
        r"\.*(salut|bonjour|bonsoir|hello|hey|hi|holla|coucou)\.*",( # pôlitesse
            "Salut, ça va ?", "Bonjour, quoi de neuf ?", "Hey, comment vas-tu ?", "Ca roule ?"
        )
    ),(
        r".*(ça|ca) va.*\?",( # formules de pôlitesse
            "Cool, et toi ?", "Je vais bien merci et toi ?", "Très bien! Toi ?"
        )
    ),(
        r".*et toi.*\?",( # relances à la machine
            "Je suis toujours chargé, parlons de toi", "Comme d'hab, mais intéressons nous à toi"
        )
    ),(
        r"(.*).*(étais|vais|irai|allé|aller|parti|partir|venu|venir) (à|au|aux|chez) (.*)",( # lieux
            "%2 ? C'est loin ça ?", "Pourquoi aller %3 %4 ?",
            "Ca se situe où %4 ?", "Comment tu te rends %3 %4 ?"
        )
    ),(
        r"j'ai fait (.*)",( # activités
            "Super activité ! Explique moi un peu",
            "Et ça consiste à faire quoi précisement ?",
            "Alors, les résultats ?", "C'est quoi %1 ?"
        )
    ),(
        r"pourquoi (.*)(\??)",( # question ouverte
            "Pourquoi pas ?",
            "Tu penses que %1 ?", "Pourquoi d'après toi ?",
            "J'ai une petite idée, et toi ?"
        )
    ),(
        r".*(parce que|car|puisque)(.*)(\!?)",( # réponse ouverte
            "Je suis d'accord, mais développe un peu",
            "Oui, en effet %1. Mais encore ?",
            "Hum... continue s'il te plaît"
        )
    ),(
        r"(.*)\?",( # toutes les autres questions
            "Toi, tu en penses quoi ?",
            "%1 ... bonne question, t'en dis quoi ?",
            "A ton avis ?"
        )
    ),(
        r"oui(.*)",( # affirmatif
            "T'as raison, sinon ?",
            "%1 bon bon bon. Autrement ?", "Cool alors"
        )
    ),(
        r"non(.*)",( # négatif
            "Et pourquoi ça ?",
            "%1 ah non?", "Oh, tu peux développer ?"
        )
    ),(
        r"quit",( # phrase de fin
            "Cool, à plus !", "Bonne continuation alors", "Tchao !",
            "Salut l'ami.e !"
        )
    ),(
        r"(.*)",( # phrases de relances
            "%1 tu dis ? Développe un peu",
            "Dis-m'en plus", "Raconte moi tout, c'est pas assez ça !",
            "%1 ? C'est tout ? Et les détails ?", "Mais encore ?",
            "Cool ça. Parle moi un peu de ta journée.", "Intéressant, ensuite ?",
            f"Bien. Il est {datetime.now().strftime('%H:%M')}, tu fais quoi après ?"
        )
    ),
]


# In[5]:


chatbot = Chat(pairs, reflect)


# In[6]:


def chat():
    global chatbot
    print(art)
    print(f"{'='*70}\nBonjour! Je suis le Chatbot français avec qui tu peux parler de ta journée")
    print("Tape 'quit' si tu veux partir :)")
    chatbot.converse()
    print('='*70)


# In[7]:

if __name__ == "__main__":
    chat()

