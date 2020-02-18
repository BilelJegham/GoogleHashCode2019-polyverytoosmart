# -*- coding: utf-8 -*-

from .RouterPlacer import RouterPlacer
from packages.structure.Map import Map
from packages.utils.log import log
from random import randint
from math import sqrt


class AlgoPlacementAleatoire(RouterPlacer):


    def __init__(self, problem):
        self.problem = problem
        self.routers = []
        self.backbones = []

    def place_router(self):
        """
        Cette fonction permet de placer aléatoirement les routeurs et de les relier tant que le budget maximum
        n'est pas atteint """
        log("Debut du placement aleatoire")

        height = len(self.problem.map.cells[0])
        width = len(self.problem.map.cells)

        # On initialise la premier positon à relier soit la bb de départ
        previous_pos = (self.problem.map.backbone_source_pos.x,self.problem.map.backbone_source_pos.y)
        cost = 0

        while cost <= self.problem.budget_max: # Tant que le coût ne dépasse pas le budget maximum
            x = randint(0,width-1)
            y = randint(0,height-1)
            pos_r = (x,y)

        # La boucle if permet de placer un routeur sur la map en fonction des coordonnees tirées aléatoirement juste avant
        # si la cellule en question est une TARGET et si elle n'est pas dans la liste des routeurs posés
            if self.problem.map.cells[x][y].is_target() and (x,y) not in self.routers:
        # On fait appel a la fonction relier qui permet de trouver le chemin le plus court entre le routeur posé et le backbone source
                way = self.relier(previous_pos, pos_r)
                previous_pos = pos_r
        # On calcul le coût de pose du routeur et des backbones et on l'ajout au coût total
                cost_backbone = self.problem.bb_cost * len(way)
                cost_router = self.problem.router_cost
                cost += cost_backbone + cost_router
        # On vérifie à nouveau que le coût est inférieur au budget maximum avant d'ajouter les coordonnees des routeurs
        # et des backbones à nos listes, pour eviter un dépassement de budget
                if cost <= self.problem.budget_max:
                    self.routers.append(pos_r)
                    self.backbones += way
        # Si les coordonnees du backbone source sont deja dans la liste, on les supprime pour eviter un doublon
        if self.problem.map.backbone_source_pos in self.backbones :
            self.backbones.remove(self.problem.map.backbone_source_pos)
        log("Fin du placement aleatoire")
        return (self.routers, self.backbones)


    def distance_2_points(self,a,b):
        """
        Cette fonction permet de calculer la distance entre 2 points a et b de la map.
        """
        d = sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)
        return d


    def relier(self,caseDepart,caseDestination):
        """
        Cette fonction renvoit la liste des cases entre les points a et b.
        """
        caseActuelle = caseDepart
        chemin = list() # Contient la liste des positions
        while not (caseActuelle[0] == caseDestination[0] and caseActuelle[1] == caseDestination[1]): # Tant que nous n'arrivons pas à la case de destination
        # On liste les possibilitées de case autour de notre point
            possibilite = list() # Liste toutes les possibilitées
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if not(i==0 and j==0):
                        possibilite.append((caseActuelle[0]+i,caseActuelle[1]+j))

        # On selectionne la case la plus proche de la case de destination
            min, cmin = None,None # Min contient la distance, et cmin la position de la case en question
            for case in possibilite:
                val = self.distance_2_points(case, caseDestination)
                if(min==None or val<min):# si il n'y pas encore de minimum ou si la distance est inférieur à la valeur minimale actuelle
                    cmin = case
                    min = val
            caseActuelle = cmin #
            if caseActuelle not in self.backbones:
                chemin.append(caseActuelle)
        return chemin
