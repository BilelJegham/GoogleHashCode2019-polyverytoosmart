# -*- coding: utf-8 -*-

from .RouterPlacer import RouterPlacer
from packages.structure.Map import Map
from packages.utils.log import log
from packages.solving.AlgoBackbonePrim import AlgoBackbonePrim

class AlgoRouter2R(RouterPlacer):
    """Placement des routeurs sur un quadrillage de taille 2*R (R = portée d'un routeur)"""

    def __init__(self, problem):
        self.problem = problem
        self.routers = []
        self.limitBudget = False#True si activation de la limite de budget
        self.stopPlacement = False

    def partial_place(self, max_x, max_y, inc_x, inc_y):
        """Placement de routeurs sur un quart de la carte totale"""
        backbone = self.problem.map.backbone_source_pos
        x = backbone.x
        y = backbone.y
        r = self.problem.router_range

        while 0 < y < max_y:
            while 0 < x < max_x:
                if self.problem.map.cells[x][y].is_target() and (x, y) not in self.routers :
                    if not(self.limitBudget) or self.__testCout((x, y)): #Si il n'y a l'activation de la limite de budget ou si le budget n'est pas dédépassé
                        self.routers.append((x, y))
                    else:
                        log("Dépasssement budget arret de placement des routeurs", "warn")
                        return
                x = x + (2*r if inc_x else -2*r)
            x = backbone.x
            y = y + (2*r if inc_y else -2*r)

    def place_router(self, limitBudget=False):
        """Placer les routeurs"""
        log("Placement des routeurs avec la technique 2R")
        self.limitBudget = limitBudget # Active ou non la limite de budget
        self.routers = []
        map = self.problem.map
        backbone = map.backbone_source_pos
        height = len(map.cells[0])
        width = len(map.cells)

        # Schéma de placement par rapport au backbone (+)
        # A | B
        # --+--
        # C | D
        self.partial_place(backbone.x+1, backbone.y+1, False, False) # A
        self.partial_place(width, backbone.y+1, True, False) # B
        self.partial_place(backbone.x+1, height, False, True) # C
        self.partial_place(width, height, True, True) # D

        # Suppression du backbone (on ne peut pas placer de routeur sur le backbone)
        if (backbone.x, backbone.y) in self.routers:
            self.routers.remove((backbone.x, backbone.y))

        return self.routers


    def __testCout(self, pos):
        """
        On voit si l'ajout d'un routeur fera dépassée le budget
        True si placement possible false sinon
        """
        if self.stopPlacement :#Si le budget a été dépassé pas la peine de placer un nouveau routeur
            return False
        listRouterTemp = self.routers[:] # On copie liste des routeurs pour effectuer l'estimation du cout de placement
        listRouterTemp.append(pos) # on ajoute la position du nouveau routeurs
        coutPlacementRouteur = len(listRouterTemp)* self.problem.router_cost # on ajoute le cout du nouveau routers
        #On crée une instance de placement de BB
        backbone_place = AlgoBackbonePrim(self.problem.map.backbone_source_pos,listRouterTemp)
        backbones = backbone_place.place_backbone(False)

        coutPlacementBackbone = self.problem.bb_cost*len(backbones)# on ajoute le cout de placement des BB

        if (coutPlacementRouteur+coutPlacementBackbone) > self.problem.budget_max:#budget dépassé arrêter de placer
            self.stopPlacement = True
            return False
        return True
