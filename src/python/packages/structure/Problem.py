# -*- coding: utf-8 -*-

from packages.io.Solution import Solution
from packages.solving.AlgoBackbonePrim import AlgoBackbonePrim
from packages.solving.AlgoRouter2R import AlgoRouter2R
from packages.utils.log import log
from packages.solving.AlgoPlacementAleatoire import AlgoPlacementAleatoire



class Problem:
    """
    Représente le problème posé.
    A à sa disposition toutes les informations nécessaires à sa résolution.

    """

    def __init__(self, router_range, bb_cost, router_cost, budget_max, map):
        """
            Constructeur
            :param router_range: portée d'un routeur
            :param bb_cost: prix du backbone
            :param router_cost: prix du routeur
            :param budget_max: le budget maximale
            :param map: la carte à analyser et traiter
        """
        self.router_range = router_range
        self.bb_cost = bb_cost
        self.router_cost = router_cost
        self.budget_max = budget_max
        self.map = map

    def solve(self):
        """
        Résout le problemes en plaçant les routeur et les blackbones
        :return: une représentation structurée de la solution
        :rtype: Solution
        """
        router_place2R = AlgoRouter2R(self)

        routers = router_place2R.place_router()
        backbone_place = AlgoBackbonePrim(self.map.backbone_source_pos,routers)
        backbones = backbone_place.place_backbone()

        solution = Solution(routers,backbones)
        cost = Solution.calculate_cost(len(backbones), len(routers), self.bb_cost, self.router_cost)
        part_budget = (cost*100)/self.budget_max #Part du budget utilisé
        if part_budget > 100: #Si tout le budget a été utilisé (+100%)
            # Probleme d'accent pour l'intégration continue
            log("Le cout " + str(cost) + " excedant. (budget max : "+str(self.budget_max)+")", "error")
            log("Recalcul de la solution avec limite de budget")
            routers2 = router_place2R.place_router(True)
            backbone_place2 = AlgoBackbonePrim(self.map.backbone_source_pos,routers2)
            backbones2 = backbone_place2.place_backbone()
            solution = Solution(routers2,backbones2)
        elif part_budget < 50 and len(self.map.cells)<300:#Si moins de 50 % du budget a été utilisé et si la carte n'est pas trop grande
            log(str(int(part_budget))+"% budget utilisé, Recalcul","warn")
            router_placeAlea = AlgoPlacementAleatoire(self)
            routers, backbones =  router_placeAlea.place_router()
            #Optimisation placement des cables
            backbone_place = AlgoBackbonePrim(self.map.backbone_source_pos,routers)
            backbones = backbone_place.place_backbone()
            solution = Solution(routers,backbones)
        else:
            log("Le cout revient a " + str(cost))

        return solution
