# -*- coding: utf-8 -*-

from packages.utils.log import log

class Solution:
    """
        Cette classe permet de représenter la solution au probleme de palcement
    """
    def __init__(self,l):
        """
            Constructeur
        """
        self.list = l


    def write(self, file):
        """
            Ecrit le fichier de sortie
            :param: String nom du fichier
        """
        log('Ecriture de la solution dans : '+file)
        # map = self.map
        l = self.list
        fichier = open(file, "w")
        #Ecriture position des Blackbone
        fichier.write(str(len(l))+"\n")
        for lib in l:
            fichier.write(str(lib[0])+" "+str(lib[1])+"\n")
            fichier.write(" ".join(str(x) for x in lib[2]) +"\n")

        log("Fin de l'Ecriture")



if __name__ == '__main__':
    lCell = list()
    for x in range(2):
        lCelly = list()
        for y in range(2):
            c = Cell(None,True)
            lCelly.append(c)
        lCell.append(lCelly)
    map = Map(lCell,(0,0))
    sol =  Solution()
    sol.setMap(map)
    sol.write("test.txt")
    cost = Solution.calculate_cost(3, 2, 1, 100)
    print(cost)
