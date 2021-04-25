import numpy as np
from pprint import pprint
import pandas as pd
#aristas = [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 1), (4, 5), (4, 6), (5, 0), (5, 2), (5, 6), (6, 0), (6, 1), (6, 3)]

#num_nodos = 1 + max([max(a, b) for a, b in aristas])

#dist = {(a, b): -1 for a in range(num_nodos) for b in range(num_nodos)}

# def distancia(a, b):
#     d = 1
#     # Si la distancia ES una arista, devuelvo 1
#     if (a, b) in aristas or (b, a) in aristas:
#         if dist[(a,b)] == -1 or dist[(a,b)] > d:
#             # Guardo el valor
#             dist[(a,b)] = d
#         return d
#
#     # Calculo todas las distancias
#     aristas = aristas.copy()
#     # Si no, "arranco" de a y "llego" a b
#     for x, y in aristas:
#         d = 1
#         if x==a or y==a:
#             # Arranco de a
#             d += 1 + calcular_distancia(x, y, aristas.copy().remove((x,y)))
#
#         if dist[(x,y)] == -1 or dist[(x,y)] > d:
#             dist[(x,y)] = d
#
#     print(dist)


class Grafo():
    def __init__(self):
        aristas = [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (2, 6), (3, 0), (3, 4), (3, 5), (4, 1), (4, 5), (4, 6), (5, 0), (5, 2), (5, 6), (6, 0), (6, 1), (6, 3)]
        #aristas = [(0, 1), (0, 14), (0, 15), (1, 2), (1, 11), (2, 3), (2, 7), (3, 4), (3, 16), (4, 5), (4, 14), (5, 6), (5, 10), (6, 7), (6, 17), (7, 8), (8, 9), (8, 13), (9, 10), (9, 18), (10, 11), (11, 12), (12, 13), (12, 19), (13, 14), (15, 16), (15, 19), (16, 17), (17, 18), (18, 19)]
        
        #aristas = [(0, 1), (1, 2), (2, 3), (3, 4)]
        # Convierto tuplas a conjuntos
        self.aristas = [{x, y} for x, y in aristas]
        # Asumo que existen todos lo]s nodos del 1 al max de aristas
        # n: Numero de nodos
        self.n = 1 + max([max(a, b) for a, b in self.aristas])
        #pd.set_option("display.max_rows", self.n, "display.max_columns", self.n)
        pd.set_option('display.max_rows', self.n)
        pd.set_option('display.max_columns', self.n)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

        self.null = np.nan
        
        # Inicializo diccionario con todas las combinaciones de nodos
        #self.dist = {(a, b): self.null for a in range(self.n) for b in range(self.n)}
        # Lleno diagonal de ceros, pues nunca los visito como nodos
        self.dist = {(a, a): 0 for a in range(self.n)}

        #pprint(self.dist)
        
        

    def mostrar(self):
        #distancias = self.null * np.ones(shape=(self.n, self.n), dtype=np.int)
        #distancias = [[0] * self.n]*self.n
        distancias = pd.DataFrame(self.null * np.ones(shape=(self.n, self.n)), dtype="Int64")

        for xy, dist in self.dist.items():
            x, y = xy
            distancias[x][y] = dist
            distancias[y][x] = dist

        print(distancias)


    def distancia(self, a, b):

        if self.dist[(a,b)] == self.null:
            self.calcular_distancia(a,b, self.aristas)
        
        return self.dist[(a,b)]

    def cd(self, a, b):
        print(self.aristas)
        busco_a = True
        #busco_b = False
        busco_x = False
        dist = 0
        x=0
        y=0
        for i, arista in enumerate(self.aristas):
            print("i={}".format(i))
            for j in range(i, len(self.aristas)):
                print("j={}".format(j))
                # Esta a en arista?
                if busco_x and x in self.aristas[j]:
                    print("Encontre x={}! i={}, dist={}".format(x, i, dist))
                    dist += 1
                    y = self.aristas[j].copy()
                    y.remove(x)
                    y = y.pop()
                    if y == b:
                        # Gane!
                        print("Gane! Distancia:", dist)
                        return dist
                    else:
                        x = y

                if busco_a and a in arista:
                    print("Encontre a! i={}, dist={}".format(i, dist))
                    
                    busco_a = False
                    busco_x = True
                    x = arista.copy()
                    x.remove(a)
                    x = x.pop()
                    print("Busco x={}".format(x))
                    dist +=1
                    


    def calcular_distancia(self, a, b, aristas, d=1):

        print("aristas:", aristas)
        # Si la distancia ES una arista, devuelvo 1
        if (a, b) in self.aristas or (b, a) in self.aristas:
            if self.dist[(a, b)] == self.null or self.dist[(a, b)] > d:
                self.dist[(a, b)] = d
                self.dist[(b, a)] = d
            return d
        
        # Calculo todas las distancias
        # Si no, "arranco" de a y "llego" a b
        aristas = self.aristas.copy()
        for x, y in aristas:
            
            aristas.remove((x, y))

            if x==a or y==a:
                # Arranco de a hasta x o y, y busco b
                # (a, x), (x, j), (j, k), (k, b)
                d = self.calc_dist_recur(x, b, aristas, d+1)

            
            if self.dist[(x,y)] == self.null:
                self.dist[(x,y)] = 1
                self.dist[(y,x)] = 1

            

            aristas.append((x,y))
            
        print(self.dist)

    def calculo_de_distancia(self, a, b, aristas, d=0):
        
        # Caso 0: Son iguales
        if a == b:
            return d

        # Caso 1: Son vecinos
        d += 1
        if {a, b} in self.aristas:
            if (a, b) not in self.dist.keys():
                self.dist[(a, b)] = 1
                self.dist[(b, a)] = 1
            return 1

        # Caso 2: Hay al menos un nodo intermedio
        dist_inicios = []
        for i, aris in enumerate(aristas):
            print("otro aristas:",aristas)
            d_int = d+1
            # Busco a
            sin_elem = aristas.copy()
            sin_elem.remove(aris)
            print(sin_elem)
            x = aris.pop()
            y = aris.pop()
            if x==a:
                # Se que y NO es b (pues sino Caso 1)
                # Quiero medir d(y, b)
                d = self.calculo_de_distancia(y, b, d=d_int, aristas=sin_elem)
                dist_inicios.append(d)

            print("i:",i, "d_int",d_int)
        return min(dist_inicios)

    def recorrer_hasta_b(self, a, b, d, aristas):
        print("aristas:",aristas)
        if aristas == []:
            return d

        # Caso 1: Son vecinos. Gane!
        if {a, b} in self.aristas:
            if self.dist[(a, b)] == self.null or self.dist[(a, b)] > d:
                self.dist[(a, b)] = d
                self.dist[(b, a)] = d
            return d

        # Caso 2: Hay al menos un nodo intermedio
        dist_inicios = []
        for i, aris in enumerate(aristas):
            d_int = d+1
            # Busco a
            sin_elem = aristas.copy()
            sin_elem.remove(aris)

            x = aris.pop()
            y = aris.pop()
            if x==a:
                # Se que y NO es b (pues sino Caso 1)
                # Quiero medir d(y, b)
                d = self.recorrer_hasta_b(y, b, d=d_int, aristas=sin_elem)
                dist_inicios.append(d)
        return min(dist_inicios)

    def calc_dist_recur(self, a, b, aristas, d=0):
        print(a, "->", b)
        print("Distancia:", d)
        print("Distancias: {}".format(self.dist.items()))
        # Caso 0: Son iguales
        if a == b:
            self.dist[(a, a)] = 0
            return d

        # Caso 1: Son vecinos
        d += 1
        if {a, b} in self.aristas:
            if (a, b) not in self.dist.keys():
                self.dist[(a, b)] = 1
                self.dist[(b, a)] = 1
            return d
        print("aristas_recu:", aristas)
        
        # Calculo todas las distancias
        # Si no, "arranco" de a y "llego" a b
        #aristas = self.aristas.copy()
        d0 = d
        ds = []
        for x, y in aristas:
            d=d0
            aristas_sig = aristas.copy()
            aristas_sig.remove({x, y})
            print({x, y})

            if x==b:
                # Llegue a b
                print("Encontré un camino b! era x!")

                if (y, b) not in self.dist.keys() or self.dist[(y, b)] > (d):
                    print("escribe 0")
                    self.dist[(y, b)] = d
                    self.dist[(b, y)] = d
                #return d

            if y==b:
                # Llegue a b
                print("Encontré un camino a b! era y!")
                if (x, b) not in self.dist.keys() or self.dist[(x, b)] > (d):
                    print("escribe y==b")
                    self.dist[(x, b)] = d
                    self.dist[(b, x)] = d
                #return d

            if x==a:
                print("Arranco de a:x -> hasta y")
                # Arranco de a hasta x o y, y busco b
                # (a, x), (x, j), (j, y), (y, b)
                d = self.calc_dist_recur(y, b, aristas_sig, d)
                ds.append(d)
                if (y, b) not in self.dist.keys() or self.dist[(y, b)] > (d):
                    print("escribe x==a")
                    self.dist[(y, b)] = d
                    self.dist[(b, y)] = d

            if y==a:
                print("Arranco de a:y -> hasta x")
                # Arranco de a hasta x o y, y busco b
                # (a, x), (x, j), (j, y), (y, b)
                d = self.calc_dist_recur(x, b, aristas_sig, d)
                ds.append(d)
                print("self.dist.keys()",self.dist.keys())
                if (x, b) not in self.dist.keys() or self.dist[(x, b)] > (d):
                    print("escribe y==a")
                    self.dist[(x, b)] = d
                    self.dist[(b, x)] = d

        print("ds:", ds)
        if ds == []:
            return np.inf
        else:
            return min(ds)

if __name__ == "__main__":
    g = Grafo()
    g.mostrar()
    #g.computar_diagonal()
    #g.mostrar()
    #g.computar_aristas()
    #g.mostrar()

    #print("Distancia:", g.distancia(0,3))
    print("Distancia:", g.calc_dist_recur(3, 12, g.aristas))
    g.mostrar()
