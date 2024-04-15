

"""On représente nos élements avec une classe qui va présenter plusieurs attributs"""
class Automate:
    def __init__(self,tab_automate):
        self.longueur_alphabet = tab_automate[0]
        self.nombre_etats = tab_automate[1]
        self.nombre_etats_initiaux = tab_automate[2][0]
        self.nombre_etats_finaux = tab_automate[3][0]
        self.etats_initiaux = tab_automate[2][1:]
        self.etats_finaux = tab_automate[3][1:]
        self.nombre_transitions = tab_automate[4][0]
        self.transitions = tab_automate[4][1:]


