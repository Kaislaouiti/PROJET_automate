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


"""Cette fonction va permettre de transformer notre automate en tableau on va aller remplir cette matrice par rapport à notre automate
"""

def automatetableau(automate):
    tab = [["X" for i in range(automate.longueur_alphabet + 2)] for j in
           range(automate.nombre_etats + 1)]  # On prédéfinit notre matrice
    alphabet = []

    for i in range(automate.nombre_transitions):  # On crée le tableau qui va présenter notre alphabet
        if automate.transitions[i][1] not in alphabet:
            alphabet.append(automate.transitions[i][1])
    tab[0][0] = ""
    tab[0][1] = "E/A"
    for k in range(automate.longueur_alphabet):  # On utilise ce tableau pour crée la première ligne avec les lettres
        tab[0][k + 2] = alphabet[k]

    for l in range(automate.nombre_etats):  # On regarde si les états sont des entrées ou sorties afin de le préciser
        tab[l + 1][0] = ""
        if l in automate.etats_initiaux:
            tab[l + 1][0] = "E"
        else:
            if l in automate.etats_finaux:
                tab[l + 1][0] += "S"

        tab[l + 1][1] = l  # La prémière colonne présentera les états
        for i in range(automate.nombre_transitions):

            if automate.transitions[i][0] == str(
                    l):  # Pour chaque état on va regarder les transitions qui les concernent

                for j in range(len(alphabet)):
                    if automate.transitions[i][1] == alphabet[
                        j]:  # On regarde ensuite quel lettre cette transition concerne
                        if tab[l + 1][
                            j + 2] == "X":  # Enfin on regarde si il y'a déja une transition à cet emplacement , si c'est pas le cas , on remplace de X , sinon , on ajoute la noubelle transition
                            tab[l + 1][j + 2] = automate.transitions[i][2]
                        else:
                            tab[l + 1][j + 2] = tab[l + 1][j + 2] + "," + automate.transitions[i][2]
                    continue

    return tab

"""Cette fonction va permettre d'afficher un automate grace à la fonction prédefinnie tabulate qui permet de 
transformer une matrice en un tableau dans la console 
"""
def affichage_automate_tableau(automate):
    tab=automatetableau(automate)

    print(tabulate(tab, headers="firstrow", tablefmt="grid"))







def minimisation(automate):
    tab_automate=automatetableau(automate)
    tab_sortie=tab_automate
    for i in range(1,len(tab_automate)):
        for j in range(1,len(tab_automate[i])):
            if int(tab_sortie[i][j]) in automate.etats_finaux:
                tab_sortie[i][j]="S"
            else :
                tab_sortie[i][j]="N"

    dico={}

    for i in range(1,len(tab_automate)):
        tab=tab_sortie[i][1:]
        if tab not in dico.values():

            dico[i-1]=tab
        else:
            for cle, valeur in dico.items():
                if valeur == tab:
                    if isinstance(cle, tuple):
                        nouvelle_clef = (*cle, i-1)
                    else:
                        nouvelle_clef=(cle,i-1)
                    del dico[cle]
                    dico[nouvelle_clef]=valeur
                    break

    dico_transforme={}
    lettre = ord('A')  # Utilisation de la fonction ord() pour obtenir le code ASCII de la lettre 'A'

    for cle in dico:
        # Convertir le code ASCII en caractère
        nouvelle_clef = chr(lettre)
        dico_transforme[nouvelle_clef] = cle
        lettre += 1  # Passer à la lettre suivante dans l'alphabet
    print(dico_transforme)

    lettres=["A","B","C","D","E"]
    compteur=0
    print(dico_transforme)
    tableau = [0] * (automate.nombre_etats)

    # Remplir le tableau avec les valeurs du dictionnaire transformé
    for indice, lettre in enumerate(tableau):
        for cle, valeur in dico_transforme.items():
            if isinstance(valeur, tuple):
                if indice in valeur:
                    tableau[indice] = cle+str(compteur)
                    break
            elif valeur == indice:
                tableau[indice] = cle
                break
        compteur+=1
    print(tableau)
    nouveau_tab=automatetableau(automate)
    for i in range(1,len(tab_automate)):
        for j in range(1,len(tab_automate[i])):
            nouveau_tab[i][j]=tableau[int(nouveau_tab[i][j])]

    print(nouveau_tab)

    print(tabulate(nouveau_tab, headers="firstrow", tablefmt="grid"))

