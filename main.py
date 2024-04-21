from Fonction import *

automate = creer_automate(2)
affichage_automate_tableau(automate)
determiniser_epsilon(automate)

while(1):
    print("---------Bienvenue dans le projet Automate---------")
    print("Choisissez un automate")
    numero_automate=int(input("Automate: "))
    automate = creer_automate(numero_automate)
    while(1):
        affichage_automate_tableau(automate)
        print("L'automate que vous avez choisis est :",end=" ")
        if is_standard(automate):
            print("standart",end=", ")
        else :
            print("non standart",end=", ")

        if isDeterministe(automate):
            print("determiné",end=", ")
            if isComplet(automate):
                print("complet")
            else:
                print("non complet")
        else :
            print("non determiné et non complet")
        tableau_choix=[]
        nombre_choix=4
        choix = 0

        if not(is_standard(automate)):
            tableau_choix.append("Standardiser l'automate")
            nombre_choix+=1
        if not(isDeterministe(automate)):
            tableau_choix.append("Determiniser l'automate")
            nombre_choix+=1

        else:
            if not (isComplet(automate)):
                tableau_choix.append("Completer l'automate")
                nombre_choix += 1

        tableau_choix=tableau_choix+["Donner l'automate complementaire","Minimiser l'automate","Tester si l'automate reconnait un certain mot","Choisir un nouvel automate"]
        print("choisissez une option")
        for i in range(len(tableau_choix)):
            print(i+1,tableau_choix[i])
        while(choix<1 or choix>nombre_choix):
            choix=int(input("Votre choix :"))
        choix=tableau_choix[choix-1]
        if choix in tableau_choix[:-2]:
            if choix == "Standardiser l'automate":
                print("Voici l'automate standardisé : ")
                automate_nouveau = standardiser(automate)

            elif choix == "Determiniser l'automate":
                print("Voici l'automate déterminisé : ")
                automate_nouveau = determinisation(automate)

            elif choix == "Completer l'automate":
                print("Voici l'automate complété : ")
                automate_nouveau = completer(automate)

            elif choix == "Donner l'automate complementaire":
                print("Voici l'automate complémentaire : ")
                automate_nouveau = automate_complementaire(automate)

            elif choix == "Minimiser l'automate":
                print("Voici l'automate minimisé : ")
                automate_nouveau = minimisation(automate)

            affichage_automate_tableau(automate_nouveau)
            print("Voulez vous garder ce nouvel automate pour la suite ? ")
            choix2=-1
            while(choix2!=0 and choix2!=1):
                print("0 : Oui ")
                print("1 : Non gardez l'automate avant l'application")
                choix2=int(input("votre choix : "))
            if choix2==0:
                automate=automate_nouveau
        else:
            if choix=="Tester si l'automate reconnait un certain mot" :
                continuer=1
                while (continuer):
                    mot=input("Donnez un mot :")
                    if reconaissance_mot(automate,mot):
                        print("Le mot "+mot+" est bien reconnu par l'automate")
                    else:
                        print("Le mot "+mot+" n'est pas reconnu par l'automate")
                    continuer=int(input("Tapez 0 si vous voulez arretez , sinon taper un autre chiffre pour tester un autre mot"))

            if choix=="Choisir un nouvel automate":
                break









automate1 = creer_automate(2)
affichage_automate_tableau(automate1)
automate1=completer(automate1)
affichage_automate_tableau(automate1)

automate1=minimisation(automate1)
affichage_automate_tableau(automate1)
print(reconaissance_mot(automate1,"acccabbc"))