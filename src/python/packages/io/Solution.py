# -*- coding: utf-8 -*-

from packages.utils.log import log

class Solution:
    """
        Cette classe permet de représenter la solution au probleme de palcement
    """
    def __init__(self,routers,backbones):
        """
            Constructeur
            :param routers: liste des positions des routeurs
            :param backbones: liste des positions des backbones
        """
        self.listR = routers
        self.listBB = backbones

    @staticmethod
    def calculate_cost(nb_bb, nb_routers, price_bb, price_router):
        """
            Calcul le cout de installation
            :param nb_bb: nombre de blackbone nom du fichier
            :param routers: nombre de routeur
            :param price_bb: Prix du blackbone
            :param price_router: Prix du routeur
            :return: cout d'installation
        """
        total_cost = nb_bb * price_bb + nb_routers * price_router
        return total_cost

    def write(self, file):
        """
            Ecrit le fichier de sortie
            :param: String nom du fichier
        """
        log('Ecriture de la solution dans : '+file)
        # map = self.map
        listBB = self.listBB
        listR = self.listR
        fichier = open(file, "w")
        #Ecriture position des Blackbone
        log('    - Ecriture de la position des '+str(len(listBB))+' backbones')
        fichier.write(str(len(listBB))+"\n")
        for posBB in listBB:
            fichier.write(str(posBB[0])+" "+str(posBB[1])+"\n")

        #Ecriture position des Routeurs
        log('    - Ecriture de la position des '+str(len(listR))+' routeurs')
        fichier.write(str(len(listR))+"\n")
        for r in listR:
            fichier.write(str(r[0])+" "+str(r[1])+"\n")
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
