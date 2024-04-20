"""Cette fonction va renvoyer )à partir d'un fichier contenant un automate un tableau présentant 5 cases
: taille de l'alphabet , nombre d'état , nombre état initiaux + les etats ,
 nombre états finaux plus les états , nombre de transition et les transitions"""
from tabulate import tabulate
from Automate import *
def creer_automate(numero_automate):

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
    automate=Automate(tableau)
    return automate


"""Cette fonction va permettre de transformer notre automate en tableau on va aller remplir cette matrice par rapport à notre automate
"""

def automatetableau(automate):
    tab = [["X" for i in range(automate.longueur_alphabet + 2)] for j in
           range(automate.nombre_etats + 2)]  # On prédéfinit notre matrice
    alphabet = []

    for i in range(automate.nombre_transitions):  # On crée le tableau qui va présenter notre alphabet
        if automate.transitions[i][1] not in alphabet:
            alphabet.append(automate.transitions[i][1])
    tab[0][0] = ""
    tab[0][1] = "E/A"
    for k in range(automate.longueur_alphabet):  # On utilise ce tableau pour crée la première ligne avec les lettres
        tab[0][k + 2] = alphabet[k]

    for l in range(automate.nombre_etats+1):
        # On regarde si les états sont des entrées ou sorties afin de le préciser
        tab[l + 1][0] = ""
        if l in automate.etats_initiaux:
            tab[l + 1][0] = "E"
        else:
            if l in automate.etats_finaux:
                tab[l + 1][0] += "S"

        tab[l + 1][1] = l  # La prémière colonne présentera les états


        for i in range(automate.nombre_transitions):        #On teste la longueur de la chaine de transition pour adapter selon la longueur du nombre dans les etats

            if len(automate.transitions[i])==3:
                transition1=automate.transitions[i][0]
                caractere=automate.transitions[i][1]
                transition2 = automate.transitions[i][2]
            elif len(automate.transitions[i])==4:
                if 'a' <=automate.transitions[i][1]<= 'z' :
                    transition1 = automate.transitions[i][0]
                    caractere = automate.transitions[i][1]
                    transition2 = automate.transitions[i][2:]
                else :
                    transition1 = automate.transitions[i][:2]
                    caractere = automate.transitions[i][2]
                    transition2 = automate.transitions[i][3]
            elif len(automate.transitions[i])==5:
                transition1 = automate.transitions[i][:2]
                caractere = automate.transitions[i][2]
                transition2 = automate.transitions[i][3:]
            if transition1 == str(
                    l):  # Pour chaque état on va regarder les transitions qui les concernent

                for j in range(len(alphabet)):
                    if caractere == alphabet[
                        j]:  # On regarde ensuite quel lettre cette transition concerne
                        if tab[l + 1][
                            j + 2] == "X":  # Enfin on regarde si il y'a déja une transition à cet emplacement , si c'est pas le cas , on remplace de X , sinon , on ajoute la noubelle transition
                            tab[l + 1][j + 2] = transition2
                        else:
                            tab[l + 1][j + 2] = tab[l + 1][j + 2] + "," + transition2
                    continue
    return tab

"""Cette fonction va permettre d'afficher un automate grace à la fonction prédefinnie tabulate qui permet de 
transformer une matrice en un tableau dans la console 
"""
def affichage_automate_tableau(automate):
    tab=automatetableau(automate)
    print(tabulate(tab, headers="firstrow", tablefmt="grid"))

def is_standard(automate):  # Cette méthode vérifie si l'automate est "standard" ou non

    tableau =automatetableau(automate)
    if automate.nombre_etats_initiaux != 1:  # verifie s'il n'y qune seul entrée
        return False  # Alors, cela n'est pas standard, donc on retourne False
    else:  # Sinon
        etats_initial = automate.etats_initiaux[0]  # On assigne a "etats_initiaux" la valeur de l'entrée
        etats_initial = str(etats_initial)
        for i in range(1,len(tableau)):  #on parcours le tableau a partir de la 2eme ligne jusqua la fin
            for j in range (2,len(tableau[i])): #on parcours le tableau a partir de la 3eme col jusqua la fin
                if tableau[i][j] == etats_initial  or etats_initial in tableau[i][j]:  #On verifie si il y a un etat qui rentre dans l'etat initiale
                    return False  # si c'est le cas, cela n'est pas standard, donc on retourne False
    return True  # Si aucune des conditions ci-dessus n'est satisfaite, alors cela est standard, donc on retourne True
"""Cette fonction va prendre en parametre un automate , le minimiser un automate et de le renvoyer."""

def completer(automate):

    tableau = automatetableau(automate)
    tableau.append([])
    tableau[-1].append("")
    tableau[-1].append(str(automate.nombre_etats+1))

    for i in range(1, len(tableau[0])-1):
        tableau[-1].append(str(automate.nombre_etats+1))

    for i in range(1, len(tableau)):  # on parcours le tableau a partir de la 2eme ligne jusqua la fin
        for j in range(2, len(tableau[i])):
            if tableau[i][j]=="X":
                tableau[i][j]=str(automate.nombre_etats+1)

    return tab_en_automate(tableau)


def minimisation(automate):

    tab_automate=automatetableau(automate)
    tab_sortie=tab_automate
    for i in range(1,len(tab_automate)):                    #Première étape , on transforme notre automate en tableau et on crée un nouveau tableau avec des S pour les sorties et des N pour les non sorties
        for j in range(1,len(tab_automate[i])):
            if int(tab_sortie[i][j]) in automate.etats_finaux:
                tab_sortie[i][j]="S"
            else :
                tab_sortie[i][j]="N"

    dico={}

    for i in range(1,len(tab_automate)):                    # Ensuite on va crée un dictionnaire pour regrouper les états ayant la meme ligne avec les s et n
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
    lettre = ord('A')  # Ensuite on va transformer ce tableau pour avoir les états similaire et les associer à une lettre

    for cle in dico:
        # Convertir le code ASCII en caractère
        nouvelle_clef = chr(lettre)
        dico_transforme[nouvelle_clef] = cle
        lettre += 1

    lettres=["A","B","C","D","E"]
    compteur=0
    tableau = [0] * (automate.nombre_etats+1)               #On va ensuite crée un tableau présentant tous les états avec des lettres

                                                           # On remplot le tableau avec les valeurs du dictionnaire transformé
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

    nouveau_tab=automatetableau(automate)                           #On crée notre dernier tableau qui va copier le tableau de base et on le superpose à notre tableau avec les lettres pour avoir notre tableau de lettre
    for i in range(1,len(tab_automate)):
        for j in range(1,len(tab_automate[i])):
            nouveau_tab[i][j]=tableau[int(nouveau_tab[i][j])]

    for i in range(1,len(nouveau_tab)):
        compteur = i+1

        ligne= nouveau_tab[i]
        while compteur<len(nouveau_tab):                           #On regard ensuite les lignes similaires qu'on peut retirer en comparant les lettres
            pareil=1
            for k in range(1,len(nouveau_tab[i])):

                if nouveau_tab[i][k][0]!=nouveau_tab[compteur][k][0] :
                    pareil=0
            if pareil==1:
                if nouveau_tab[i][0]=="E" or nouveau_tab[compteur][0]=="E":         #On oublie pas de garder l'entrée et les sorties
                    nouveau_tab[i][0]=="E"
                if nouveau_tab[i][0]=="S" or nouveau_tab[compteur][0]=="S":
                    nouveau_tab[i][0]=="S"
                if nouveau_tab[i][0]=="ES" or nouveau_tab[compteur][0]=="ES":
                    nouveau_tab[i][0]=="ES"
                for a in range(1,len(nouveau_tab)):                                  # On modifie l'état qu'on a retirer pour mettre celui qu'on va garder dans tout le tableau
                    for b in range(2,len(nouveau_tab[a])):

                        if nouveau_tab[a][b]==nouveau_tab[compteur][1]:
                            nouveau_tab[a][b] = nouveau_tab[i][1]

                del(nouveau_tab[compteur])
            compteur+=1

        if i==(len(nouveau_tab)-1):break
    dico={}
    compteur=0
    for i in range(1, len(nouveau_tab)):                #Enfin, pour garder la cohésion du programme , on renomme nos états par des chiffres
        dico[nouveau_tab[i][1]]=compteur
        compteur+=1

    for a in range(1, len(nouveau_tab)):
        for b in range(1, len(nouveau_tab[a])):
            nouveau_tab[a][b]=dico[nouveau_tab[a][b]]



    return tab_en_automate(nouveau_tab)

"""Cette fonction à la fonction inverse de automatetableau,elle sert à transformer un tableau d'automate en un objet automate"""
def tab_en_automate(tab_automate):

    nombre_etats=len(tab_automate)-2
    taille_alphabet=len(tab_automate[0])-2
    etat_entre=[0]
    etat_sortie=[0]
    for i in range(1,len(tab_automate)):
        if tab_automate[i][0]=="E":
            etat_entre[0]+=1
            etat_entre.append(i-1)
        if tab_automate[i][0]=="S":
            etat_sortie[0]+=1
            etat_sortie.append(i-1)
        if tab_automate[i][0]=="ES":
            etat_entre[0] += 1
            etat_entre.append(i - 1)
            etat_sortie[0] += 1
            etat_sortie.append(i - 1)
    transition=[0]
    for i in range(1,len(tab_automate)):
        for j in range(2,len(tab_automate[i])):
            transition[0]+=1
            transition.append(str(i-1)+tab_automate[0][j]+str(tab_automate[i][j]))
    automate = Automate([taille_alphabet,nombre_etats,etat_entre,etat_sortie,transition])
    return automate



def reconaissance_mot(automate,mot):
    tab_automate=automatetableau(automate)
    pointeur=str(automate.etats_initiaux[0])
    for lettre in mot:
        if ord(lettre)-97>=automate.longueur_alphabet:
            print("lettre inconnu")
            return False
        i=ord(lettre)-97+2
        pointeur=tab_automate[int(pointeur)+1][i]
        if pointeur=="X":
            return False
    if tab_automate[int(pointeur)+1][0]=="S" or tab_automate[int(pointeur)+1][0]=="ES":
        return True
    else :
        return False


