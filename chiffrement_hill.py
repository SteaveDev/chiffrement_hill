#chiffrement de Hill

def estPremier(nb1,nb2):  #nb2 est ici le modulo
    reste=-1
    while reste!=0:
        quotient=(int)(nb1/nb2)    #quotient arrondit a l'inférieur
        reste=nb1-nb2*quotient     #reste du quotien
        if(reste==1):
            return True
        nb1=nb2                  #on met nb2 dans nb1
        nb2=reste               # on met le reste dans nb2 pour faire tourner l'agorithme d'Euclide
    return False

def pgcd_inverse(nb1, nb2): #def inverse(nb,modulo):
    if(estPremier(nb1,nb2)):
        tab=dict()
        reste=1
        while(reste!=0):            #tant que reste est different de 0 on continue
            tab1=dict()
            tab1[len(tab1)]=nb1     #1ere valeur du 2eme tableau[indice]= a
            tab1[len(tab1)]=nb2     #2eme valeur du 2eme tableau[indice] = b
            tab1[len(tab1)]=nb1-(int)(nb1/nb2)*nb2  #3eme valeur du 2eme tableau[indice] = r
            tab1[len(tab1)]=(int)(nb1/nb2)  #4eme valeur du 2eme tableau[indice] = q
            reste=tab1[2]           #moyen de sortie de la boucle
            nb1=nb2                 #affectation de nb1 pour les calculs suivant de tableau[indice+1]
            nb2=reste               #affectation de nb2 pour les calculs suivant de tableau[indice+1]
            tab[len(tab)]=tab1      #affecte le tableau temporaire au premier tableau

        tab[len(tab)-1][4]=0    #on accede a la derniere case du tableau 'u=0'
        tab[len(tab)-1][5]=1    #on accede a la derniere case du tableau 'v=1'
        indice=len(tab)-2       #indice = avant derniere case du tableau

        while(indice>=0):
            tab[indice][4]=tab[indice+1][5]     #tab[indice] = ancienne valeur de v
            tab[indice][5]=-tab[indice][3]*tab[indice][4]+tab[indice+1][4]  #tab[indice] = quotient de la ligne * u(new) + u(old)
            indice-=1   #on remonte vers le haut du tableau pour atteindre les valeurs nb1 et nb2
        if(tab[0][0]>tab[0][1]):
            return tab[0][5]
        else:
            return tab[0][4]

def inverseMatrice(matrice):
    detA=(matrice[0][0]*matrice[1][1]-matrice[1][0]*matrice[0][1])%26        #formule pour avoir le det a*d-b*c
    pgcd_inv=pgcd_inverse(detA,26)                       #on inverse le det
    matrice2=dict()                             #initialisation de la matrice a retourner
    matrice2[0]=dict()  #premiere ligne de la matrice 'a' et 'b'
    matrice2[1]=dict()  #seconde ligne de la matrice 'c' et 'd'
    matrice2[0][0]=((matrice[1][1]*pgcd_inv)%26)         #produit scalaire % 26
    matrice2[0][1]=(-(matrice[0][1]*pgcd_inv)%26)
    matrice2[1][0]=((-(matrice[1][0])*pgcd_inv)%26)
    matrice2[1][1]=((matrice[0][0]*pgcd_inv)%26)
    return matrice2

def decryptage(chaine,mat):
    tab=dict()
    tab[len(tab)]=dict()    #tableau dans un tableau
    for i in range(len(chaine)):
        tab[0][len(tab[0])]=ord(chaine[i])-65     #on passe d'une chaine a un nombre

    tab[len(tab)]=dict()
    for i in range(0,len(chaine),2):    #on
        tab[1][i]=dict()
        tab[1][i][0]=tab[0][i]
        if(len(chaine)%2==1 and i==len(chaine)-1):    #si le nombre de caractere n'est pas pair
            tab[1][i][1]=0
        else:
            tab[1][i][1]=tab[0][i+1]

    tab[len(tab)]=dict()        #tableau dans un tableau
    for i in range(0,len(tab[0]),2):
        matrice_temp=dict()     #tableau temporaire
        inv_matrice_temp = inverseMatrice(mat)
        vecteurX_temp = tab[1][i]
        matrice_temp[len(matrice_temp)]=(inv_matrice_temp[0][0]*vecteurX_temp[0]+inv_matrice_temp[0][1]*vecteurX_temp[1])%26       #produit matriciel puis convertion modulo 26
        matrice_temp[len(matrice_temp)]=(inv_matrice_temp[1][0]*vecteurX_temp[0]+inv_matrice_temp[1][1]*vecteurX_temp[1])%26
        tab[2][i]=matrice_temp

    tab[3]=dict()       #tableau dans un tableau
    for i in range(0,len(tab[0]),2):
        tab[3][i]=tab[2][i][0]  #On affecte a tab[3][i] la premiere valeur du couple
        tab[3][i+1]=tab[2][i][1]    #On affecte a tab[3][i+1] la deuxieme valeur du couple

    if(tab[3][0]==14 and tab[3][1]==13 and tab[3][2]==13):      #debut de message crypter 'ONN'

        nbConsonne=0
        for i in range(0,len(tab[3])):
            if(tab[3][i]==0 or tab[3][i]==4 or tab[3][i]==8 or tab[3][i]==14 or tab[3][i]==20 or tab[3][i]==24):    #si on trouve une voyelle on remet nbconsonne a 0
                nbConsonne=0
            elif(nbConsonne>3): #si il y a plus de 4 consonnes
                break
            else:
                nbConsonne = nbConsonne + 1
        if(nbConsonne<4):   #si il y a moins de 4 consonnes dans la chaine
            conversion_chaine=""
            for i in range(0,len(tab[3])):  #alors on converti la chaine en nombre
                conversion_chaine+=chr(tab[3][i]+65)
            print(conversion_chaine)

def main():
    matrice=dict()
    matrice[0]=dict()   #premiere ligne de la matrice
    matrice[1]=dict()   #seconde ligne de la matrice
    for a in range(0,26):   #on boucle toute les combinaisons possible
        for b in range(0,26):
            for c in range(0,26):
                for d in range(0,26):
                    matrice[0][0]=a
                    matrice[0][1]=b
                    matrice[1][0]=c
                    matrice[1][1]=d
                    detA=(matrice[0][0]*matrice[1][1]-matrice[1][0]*matrice[0][1])%26
                    if(estPremier(detA,26)):
                        decryptage("ZVMBNJYDKMLJSLWZCXJBVHGK",matrice)

main()
