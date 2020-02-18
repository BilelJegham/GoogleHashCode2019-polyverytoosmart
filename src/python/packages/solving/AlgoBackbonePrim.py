# -*- coding: utf-8 -*-

from packages.solving.BackbonePlacer import BackbonePlacer
from packages.utils.log import log

class AlgoBackbonePrim(BackbonePlacer):
    '''Placement des backbones entre les routeurs selon l'algorithme de Prim'''

    def __init__(self, bbStart,routers):
        #On prend en entree les positions des routeurs precedemment calculees
        self.routers = routers
        self.bbStart = bbStart
        self.routers.insert(0,bbStart)#Ajout de la BB de départ
        #On va chercher a calculer les positions des backbones reliant les routeurs
        self.backbones = []


    def distance_routers(self):
        '''
        Calculer les distances entre les routeurs
        (distance = nombre de backbones à placer pour relier deux routeurs)

        :return: distances entre les routeurs
        :rtype: liste à deux dimensions d'entiers positifs ou nuls
        '''

        #On initialise un tableau vide à deux dimensions
        n = len(self.routers)
        dist = []
        for i in range(n):
            dist.append([None]*n)

        #On remplit le tableau avec les distances entre chaque routeurs
        for i in range(n):
            for j in range(i+1,n):
                #On utilise les variables a et b pour simplifier la formule
                a = self.routers[i]
                b = self.routers[j]
                dist[i][j] = abs(abs(b[0]-a[0]) - abs(b[1]-a[1])) + min(abs(b[0]-a[0]), abs(b[1]-a[1])) + 1
        return dist


    def Prim(self):
        '''
        Définir l'arbre couvrant minimal selon l'algorithme de Prim

        :return: arêtes de l'arbre
        :rtype: liste de tuples d'entiers
        '''

        #--------------------INITIALISATION--------------------#
        #On calcule les distances entres les routeurs
        distance = self.distance_routers()

        #On définit le point de départ
        x0 = self.routers[0]
        n = len(self.routers)

        #On initialise les listes qu'on va utiliser
        pred, dist = [], [] #Prédécesseur et distance de chaque noeud
        X = [] #Noeuds déjà dans l'arbre
        edges = [] #Arêtes dans l'arbre

        #On remplit ces listes avec les valeurs de départ
        for i in range(n):
            pred.append(None)
            dist.append((pow(10,10)))

        #On remplit les listes avec les informations du point de départ
        pred[0] = 0
        dist[0] = 0

        #On ajoute le point de départ à la liste des noeuds déjà dans l'arbre
        X.append(0)


        #--------------------ETAPE K--------------------#
        #On réitere cette étape jusqu'à ce que tous les noeuds soient dans l'arbre :
        while len(X) < len(distance):

            #On met à jour pred et dist
            for i in range(n):
                if i not in X:
                    if (distance[i][X[len(X)-1]] != None and distance[i][X[len(X)-1]] < dist[i]):
                        pred[i] = X[len(X)-1]
                        dist[i] = distance[i][X[len(X)-1]]
                    elif (distance[X[len(X)-1]][i] != None and distance[X[len(X)-1]][i] < dist[i]):
                        pred[i] = X[len(X)-1]
                        dist[i] = distance[X[len(X)-1]][i]

            #On cherche le noeud minimisant dist pour l'ajouter à l'arbre
            temp = (pow(10,10))
            for i in range(n):
                if dist[i] < temp and i not in X:
                    next = i
                    temp = dist[next]

            #On ajoute ce noeud et l'arête le reliant à l'arbre aux listes X et edges
            X.append(next)
            edges.append((pred[next], next))


        #--------------------FIN--------------------#
        #On renvoie la liste des arêtes de l'arbre
        return(edges)


    def place_backbone(self, print_log = True):
        '''
        Placer les backbones

        :return: position des backbones
        :rtype: liste de tuples d'entiers correspondant aux coordonnées des backbones
        '''

        #On recherche les arêtes reliant les routeurs
        edges = self.Prim()

        #On va placer des backbones modélisant chacune de ces arêtes
        for e in edges:
            #On récupère les coordonnées des deux routeurs pour chaque arête
            nb_r1, nb_r2 = e[0], e[1]
            r1, r2 = self.routers[nb_r1], self.routers[nb_r2]
            x1, y1, x2, y2 = r1[0], r1[1], r2[0], r2[1]

            #On ajoute les coordonnées du premier routeur à la liste, si elles n'y sont pas déjà
            if (x1, y1) not in self.backbones:
                self.backbones.append((x1, y1))

            #On se déplace jusqu'au deuxième routeur
            while x1 != x2 or y1 != y2:
                if x1 < x2:
                    x1 += 1
                elif x1 > x2:
                    x1 -= 1
                if y1 < y2:
                    y1 += 1
                elif y1 > y2:
                    y1 -= 1

                #A chaque déplacement, on ajoute les coordonnées à la liste si elles n'y sont pas déjà
                if (x1, y1) not in self.backbones:
                    self.backbones.append((x1, y1))
        #On supprime la BB de départ à la liste des routeurs
        self.routers.remove(self.bbStart)
        self.backbones.remove(self.bbStart)#la BB de départ n'a pas besoins de cable
        if print_log :
            log("Placement des backbones avec l'algorithme de Prim")
        return self.backbones


if __name__ == '__main__':
    routeurs = [(0,0),(4,5),(6,3),(11,2),(3,10),(15,15),(19,19)]
    Solution = AlgoBackbonePrim(routeurs)
    backbones = Solution.place_backbone()
    print (backbones)
