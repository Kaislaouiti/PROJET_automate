"""Cette fonction va renvoyer )à partir d'un fichier contenant un automate un tableau présentant 5 cases
: taille de l'alphabet , nombre d'état , nombre état initiaux + les etats ,
 nombre états finaux plus les états , nombre de transition et les transitions"""
from tabulate import tabulate

def creer_tableau(numero_automate):

    # On importe les lignes du fichiers
    with open("test_automate"+str(numero_automate)+".txt","r") as f:
        contenu=f.readlines()

    # Premier élément: nombre de symboles de l'alphabet
    #strip permets d'enlever le retour à la ligne , on transorme bien le caractère en int
    nb_symboles = int(contenu[0].strip())

    # Deuxième élément: nombre d'états
    nb_etats = int(contenu[1].strip())

    etats_initiaux = list(map(int, contenu[2].strip().split()))

    etats_finaux = list(map(int, contenu[3].strip().split()))

    # Cinquième élément: transitions
    nb_transitions = int(contenu[4].strip())
    transitions = [transition.strip() for transition in contenu[5:]]

    # On assemble nos élements pour crée un tableau
    tableau = [nb_symboles, nb_etats,  etats_initiaux,  etats_finaux,
               [nb_transitions] +transitions]

    return tableau


"""Cette fonction va permettre d'afficher un automate grace à la fonction prédefinnie tabulate qui permet de 
transformer une matrice en un tableau dans la console , on va aller remplir cette matrice par rapport à notre automate
"""
def affichage_automate_tableau(automate):

    tab=[["X" for i in range(automate.longueur_alphabet+1)]for j in range(automate.nombre_etats+1)] #On prédéfinit notre matrice
    alphabet=[]

    for i in range(automate.nombre_transitions):                            #On crée le tableau qui va présenter notre alphabet
        if automate.transitions[i][1] not in alphabet:
            alphabet.append(automate.transitions[i][1])
    for k in range(automate.longueur_alphabet) :                            #On utilise ce tableau pour crée la première ligne avec les lettres
        tab[0][k+1]=alphabet[k]

    for l in range(automate.nombre_etats) :
        tab[l+1][0]=l                                                       #La prémière colonne présentera les états
        for i in range(automate.nombre_transitions):

            if automate.transitions[i][0]==str(l):                          #Pour chaque état on va regarder les transitions qui les concernent

                for j in range(len(alphabet)):
                    if automate.transitions[i][1]==alphabet[j]:             #On regarde ensuite quel lettre cette transition concerne
                        if tab[l+1][j+1]=="X":                              #Enfin on regarde si il y'a déja une transition à cet emplacement , si c'est pas le cas , on remplace de X , sinon , on ajoute la noubelle transition
                            tab[l+1][j+1]=automate.transitions[i][2]
                        else:
                            tab[l+1][j+1]=tab[l+1][j+1]+","+automate.transitions[i][2]
                    continue
    print(tabulate(tab, headers="firstrow", tablefmt="grid"))








