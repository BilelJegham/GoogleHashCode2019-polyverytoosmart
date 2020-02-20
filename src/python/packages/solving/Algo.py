# -*- coding: utf-8 -*-

class Algo:
    def __init__(self, problem):
        self.allBooks = problem.allBooks
        self.day = problem.day
        self.libraries = problem.libraries

    def solve(self):

        # Initialisation
        tempsRestantGlobal = self.day
        tempsRestant = self.day
        orderedLibrairiesFinal = []

        # 1- Trier les librairies par score
        orderedLibrairies = sorted(self.libraries, key=lambda x: x.ratio, reverse=True)

        # 2- Supprimer les librairies inutiles
        checkTemps = True
        jourActuel = orderedLibrairies[0].timeSignup

        orderedLibrairiesFinal.append(orderedLibrairies[0])
        orderedLibrairies.pop(0)
        
        while(checkTemps):
            if(len(orderedLibrairies) == 0):
                checkTemps = False
            elif(tempsRestantGlobal - orderedLibrairies[0].timeSignup > 0):
                tempsRestantGlobal -= orderedLibrairies[0].timeSignup
                jourActuel += orderedLibrairies[0].timeSignup
                orderedLibrairiesFinal.append(orderedLibrairies[0])
                ens = orderedLibrairies.pop(0)

                ens = set(ens.booksId)
                for i in range(0, len(orderedLibrairies)):
                    orderedLibrairies[i].booksId = list(set(orderedLibrairies[i].booksId) - ens)

                orderedLibrairies = self.resetRatio(orderedLibrairies, jourActuel)
            else:
                checkTemps = False


        # On ne tronque plus
        # orderedLibrairies = orderedLibrairies[:cptCheckTemps]

        # for lib in range(0,len(orderedLibrairies)-1) :
        #     print(lib)
        #     for livre in range(0,len(orderedLibrairies[lib].booksId)) :
        #         for libr in orderedLibrairies[(lib+1):len(orderedLibrairies)] :
        #             if orderedLibrairies[lib].booksId[livre] in libr.booksId :
        #                 libr.booksId.remove(orderedLibrairies[lib].booksId[livre])

        # 3- Boucle
        enregistrements = []

        
        for librairie in orderedLibrairiesFinal:
            tempsRestant = tempsRestant - librairie.timeSignup
            nbLivres = tempsRestant*librairie.skipCapacity
            if(tempsRestant < 0):
                return enregistrements
            elif (nbLivres<len(librairie.booksId)):
                newListOfBook = librairie.booksId[:nbLivres]
            else :
                newListOfBook = librairie.booksId
                nbLivres = len(librairie.booksId)
            enregistrements.append([librairie.id, nbLivres, newListOfBook])
            
            # Inscrire la premiere
        print(enregistrements)
        return enregistrements
        # print(self.allBooks)


    def resetRatio(self, liste, jourActuel):
        for l in liste:
            l.resetRatio(self.allBooks, self.day, jourActuel)
        return sorted(liste, key=lambda x: x.ratio, reverse=True)