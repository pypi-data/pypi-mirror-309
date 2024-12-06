class Persona:
    def __init__(self, nome, età):
        self.nome = nome
        self.età = età

    def presentati(self):
        print(f"Mi chiamo {self.nome} e ho {self.età} anni.")

    def invecchia(self, anni):
        self.età += anni

# Uso della classe Persona
persona = Persona("Alice", 30)
persona.presentati()  # Uscita: Mi chiamo Alice e ho 30 anni.

persona.invecchia(1)
persona.presentati()  # Uscita: Mi chiamo Alice e ho 31 anni.

########################################################

# Variabili globali per memorizzare lo stato
#%%
nome_globale = ""
età_globale = 0

def imposta_persona(nome, età):
    global nome_globale, età_globale
    nome_globale = nome
    età_globale = età

def presentati():
    print(f"Mi chiamo {nome_globale} e ho {età_globale} anni.")

def invecchia(anni):
    global età_globale
    età_globale += anni

# Utilizzo delle funzioni
imposta_persona("Alice", 30)
presentati()  # Uscita: Mi chiamo Alice e ho 30 anni.

invecchia(1)
presentati()  # Uscita: Mi chiamo Alice e ho 31 anni.
#%%
