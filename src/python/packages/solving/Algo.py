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

        # 1- Trier les librairies par score
        orderedLibrairies = sorted(self.libraries, key=lambda x: x.ratio, reverse=True)

        # 2- Supprimer les librairies inutiles
        checkTemps = True
        cptCheckTemps = 0
        while(checkTemps):
            if(cptCheckTemps >= len(orderedLibrairies)):
                checkTemps = False
            elif(tempsRestantGlobal - orderedLibrairies[cptCheckTemps].timeSignup > 0):
                tempsRestantGlobal -= orderedLibrairies[cptCheckTemps].timeSignup
                cptCheckTemps += 1
            else:
                checkTemps = False

        orderedLibrairies = orderedLibrairies[:cptCheckTemps]

        # for lib in range(0,len(orderedLibrairies)-1) :
        #     print(lib)
        #     for livre in range(0,len(orderedLibrairies[lib].booksId)) :
        #         for libr in orderedLibrairies[(lib+1):len(orderedLibrairies)] :
        #             if orderedLibrairies[lib].booksId[livre] in libr.booksId :
        #                 libr.booksId.remove(orderedLibrairies[lib].booksId[livre])

        # 3- Boucle
        enregistrements = []

        for librairie in orderedLibrairies:
            tempsRestant = tempsRestant - librairie.timeSignup
            nbLivres = tempsRestant*librairie.skipCapacity
            if (nbLivres<len(librairie.booksId))
                librairie.booksId[:nbLivres]
            else :
                nbLivres = len(librairie.booksId)

            enregistrements.append([librairie.id, nbLivres, booksId ])
            
            # Inscrire la premiere

        # print(self.allBooks)
