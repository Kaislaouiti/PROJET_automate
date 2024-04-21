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

def recuperer_transition_epsilone(tableau,etat):

    if tableau[int(etat)+1][-1]=="X":
        return []
    else :
        nombre=tableau[int(etat)+1][-1]
        if "," not in nombre:

                return [nombre]+recuperer_transition_epsilone(tableau,nombre)
        else:
            a=nombre.split(",")
            return [a[0],a[1]] + recuperer_transition_epsilone(tableau, a[0])+recuperer_transition_epsilone(tableau, a[1])


def determiniser_epsilon(automate):
    tab_automate=automatetableau(automate)
    dico={}
    for i in range(automate.nombre_etats):
        dico[i] = recuperer_transition_epsilone(tab_automate,i)
    etat_de_base=automate.etats_initiaux[0]
    pile=[]
    tab=[]
    tab.append(tab_automate[0][:-1])
    tab.append([])
    tab[1].append("E")
    tab[1].append(etat_de_base)
    for keys in dico.keys():
        dico[keys]=[keys]+dico[keys]
    for i in range(2, len(tab_automate[i]) - 1):
        tab[1].append("X")
    for i in range(2,len(tab_automate[i])-1):
        for etat in dico[etat_de_base]:
            if tab_automate[int(etat)+1][i]!="X":
                if tab[1][i]=="X":
                    tab[1][i]=tab_automate[int(etat)+1][i]
                else:
                    tab[1][i]=tab[1][i]+","+tab_automate[int(etat)+1][i]
        pile.append(tab[1][i])
    compteur=2
    tab3=[etat_de_base]
    for elemnt in pile:
        tab3.append(elemnt)
    while pile!=[]:

        if ',' not in pile[0]:
            etats=[pile[0]]
        else :
            etats=pile[0].split(",")

        tab.append([])
        tab[compteur].append("")
        if len(etats)==1:
            tab[compteur].append(etats[0])
        else:
            tab[compteur].append(etats[0]+","+etats[1])
        for i in range(2, len(tab_automate[i] )- 1):
            tab[compteur].append("X")
        for i in range(2, len(tab_automate[i] ) - 1):
            for etatss in etats :
                for etat in dico[int(etatss)]:


                    if tab_automate[int(etat) + 1][i] != "X":

                        if tab[compteur][i] == "X":
                            chaine= tab_automate[int(etat) + 1][i]

                        else:

                            if tab_automate[int(etat) + 1][i] not in chaine:
                                chaine = chaine  + "," + tab_automate[int(etat) + 1][i]
                            else:
                                chaine="X"

                        tab[compteur][i] = chaine

                        if chaine not in tab3 and chaine!="X" and etatss==etats[-1]:

                            pile.append(tab[compteur][i])
                            tab3.append(tab[compteur][i])
        compteur+=1

        pile.pop(0)

        for i in range(1,len(tab_automate)):
            if tab_automate[i][0]=="S":
                for k in range(1, len(tab_automate)):
                    if str(tab_automate[i][1]) in tab_automate[k][-1]:
                        for j in range(1,len(tab)):
                            if str(k-1) in str(tab[j][1]):
                                if tab[j][0]=="E":
                                    tab[j][0]="ES"
                                else:
                                    tab[j][0]="S"


        print(tab)
        for i in range(1,len(tab)):
            for j in range(1,len(tab[i])):
                for k in range(len(tab3)):
                    if tab[i][j]==tab3[k]:
                        tab[i][j]=k
    affichage_automate_tableau(tab_en_automate(tab))






def determinisation(automate):
    nb_etat_finaux =1
    nb_etat = automate.longueur_alphabet
    tab = [[]] #listes qui va contenir les fusions des éléments
    tab2 = [] #va contenir les transitions sous la forme 1a2


    pile =[] #pour gérer quel état on fait -> difficulté pour compter
    if  automate.nombre_etats_initiaux ==0: return #pas de début -> pas de déterminisation
    for x in range(automate.nombre_etats_initiaux):
        tab[0].append(automate.etats_initiaux[x]) #on créer le premier élément, fusions de toutes les entrées
    compteur = 0
    for x in range(automate.longueur_alphabet):
        list = []

        for y in range(len(automate.transitions)):

            if (int(automate.transitions[y][0]) in tab[0]) and ord(automate.transitions[y][1]) == (97+x):
                if int(automate.transitions[y][2]) not in list:
                    list.append(int(automate.transitions[y][2]))

        pile.append(list)
        compteur+=1
        text = "0"+chr(97+x)+str(compteur)
        tab2.append(text)
    compt = 0
    while len(pile)>0:

        if pile[0] not in tab :
            for x in range(automate.longueur_alphabet):
                list=[]
                for y in range(len(automate.transitions)):
                    if int(automate.transitions[y][0]) in pile[0] and ord(automate.transitions[y][1]) == (97 + x):
                        if int(automate.transitions[y][2]) not in list:
                            list.append(int(automate.transitions[y][2]))
                if list in pile:
                    p = pile.index(list)
                    text = str(len(tab))+chr(97+x)+str(p+len(tab))
                    tab2.append(text)
                if list in tab:
                    p = tab.index(list)
                    text = str(len(tab)) + chr(97 + x) + str(p)
                    tab2.append(text)
                if list not in pile and list not in tab:
                    pile.append(list)
                    text = str(len(tab))+chr(97+x)+str(len(pile)+len(tab)-1)
                    tab2.append(text)
            tab.append(pile[0])
        pile.pop(0)
    #ici on a les états, l'états initial et les transitions.
    #plus qu'à trouver les états finaux.
    tab_etat_finaux = []
    nb_etat = len(tab)-1
    for x in range(len(automate.etats_finaux)):
        for y in range(len(tab)):
            if automate.etats_finaux[x] in tab[y]:
                tab_etat_finaux.append(tab[y])
    for x in range(len(tab_etat_finaux)):
        tab_etat_finaux[x] = tab.index(tab_etat_finaux[x])

    liste0 = [1]+[0]
    liste1 = [len(tab_etat_finaux)] + tab_etat_finaux
    tableau = [automate.longueur_alphabet, nb_etat, liste0, liste1,
               [len(tab2)] + tab2]
    automate=Automate(tableau)
    tableau=automatetableau(automate)
    dernier_tableau=[]

    for i in range(len(tableau)):
        deja_present=0
        for j in range(len(dernier_tableau)):
            if tableau[i][0]==dernier_tableau[j][0] and tableau[i][2:]==dernier_tableau[j][2:]:
                deja_present=1
        if deja_present==0: dernier_tableau.append(tableau[i])

    return  tab_en_automate(dernier_tableau)
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
            if "," not in str(tab_automate[i][j]):
                transition[0]+=1
                transition.append(str(i-1)+tab_automate[0][j]+str(tab_automate[i][j]))
            else :
                tab=tab_automate[i][j].split(",")
                for nombre in tab:
                    transition[0] += 1
                    transition.append(str(i - 1) + tab_automate[0][j] + nombre)

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

"""Cette fonction permet de standardiser un automate (même s'il est déjà standardisé). Elle prend en entré une instance de la classe automate et renvoie une instance de cette même classe """

def standardiser(automate):
    tab_automate = automatetableau(automate)
    new_transi = ['' for i in range(automate.longueur_alphabet + 2)]        # On créer le tableau qui représentera notre nouvel état puisqu'on part du principe que l'automate n'est pas déjà standardisé
    new_transi[0] = 'E'
    new_transi[1] = len(tab_automate)-1
    new_trans_etat = []
    nombre_actuel = ''

    for j in range(2,automate.longueur_alphabet+2):     # On parcourt d'abord en ligne et ensuite en colonne
        for i in range(1,len(tab_automate)):
            if (tab_automate[i][1] in automate.etats_initiaux):
                tab_automate[i][0] = ''                                  # On enlève l'etiquette entrée aux anciens états entrées
                if (tab_automate[i][1] in automate.etats_finaux):
                    new_transi[0] = 'ES'                                # On regarde si une ancienne entrée n'étais pas aussi une sortie
                for caractere in tab_automate[i][j]:
                    if caractere.isdigit():                              # On regarde les nombres au cas ou il y a plusieurs état dans une chaine de transition
                        nombre_actuel += caractere
                    else:
                        if (nombre_actuel not in new_trans_etat) and nombre_actuel != '':
                            new_trans_etat.append(nombre_actuel)         # On met chaque nombre reconnue dans une liste en vérifiant qu'il y est pas déjà et on recommence pour chaque ligne
                        nombre_actuel = ''
                if nombre_actuel :
                    if (nombre_actuel not in new_trans_etat):
                        new_trans_etat.append(nombre_actuel)
                    nombre_actuel = ''
        if new_trans_etat == ['']:
            new_trans_etat = ['X']
        new_transi[j] = ','.join(new_trans_etat)                         # On retranscrit la liste de nombre recolté dans notre nouvel état  et on recommence pour chaque colonne
        new_trans_etat = []

    tab_automate.append(new_transi)                                      # On rajoute le nouvel état entrée
    return tab_en_automate(tab_automate)

"""Fonction pour vérifier si un automate est complet """
def isComplet(automate):
    tableau = automatetableau(automate)
    for i in range(1, len(tableau)):
        for j in range(2, len(tableau[i])):
            if tableau[i][j] == 'X':  # On verifie si ya un X dans une case
                return False
    return True

"""Fonction pour vérifier si un automate est déterministe """

def isDeterministe(automate):
    tableau = automatetableau(automate)
    if automate.nombre_etats_initiaux != 1:
        return False
    else:
        for i in range(1, len(tableau)):
            for j in range(2, len(tableau[i])):
                if "," in tableau[i][j]:  # On verifie si plusieurs états sont dans une case
                    return False
    return True

def automate_complementaire(automate):   # En suivant le modèle des autres fonctions , on inverse simplement les etats sorties et les non sorties
    tableau = automatetableau(automate)
    for i in range(1, len(tableau)):
        if tableau[i][0]=="S":
            tableau[i][0]=""
        elif tableau[i][0]=="ES":
            tableau[i][0]=="E"
        elif tableau[i][0]=="":
            tableau[i][0]="S"
        elif tableau[i][0]=="E":
            tableau[i][0]=="ES"

    return tab_en_automate(tableau)

def trace_automate(automate,num_automate):
    nom_fichier = "Trace_automate_B4-"+str(num_automate)+".txt"

    with open(nom_fichier, 'w') as fichier:
        fichier.write(str(automate.longueur_alphabet)+"\n")
        fichier.write(str(automate.nombre_etats)+"\n")
        fichier.write(str(automate.nombre_etats_initiaux)+" ")
        for i in automate.etats_initiaux:
            fichier.write(str(i)+" ")
        fichier.write("\n"+str(automate.nombre_etats_finaux)+" ")
        for i in automate.etats_finaux:
            fichier.write(str(i)+" ")
        fichier.write("\n"+str(automate.nombre_transitions)+"\n")
        for i in automate.transitions:
            fichier.write(i+"\n")




