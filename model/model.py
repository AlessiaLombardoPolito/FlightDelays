import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allAirports = DAO.getAllAirports()
        self._idMap = {}
        for a in self._allAirports:
            self._idMap[a.ID] = a
        self._grafo = nx.Graph()
        self._bestPath = []
        self._bestObjFun = 0


    def camminoOttimo(self, v0, v1 ,t):
        self._bestPath = []
        self._bestObjFun = 0

        parziale = [v0]
        self.ricorsione(parziale, v1, t)

        return self._bestPath, self._bestObjFun

    def ricorsione(self, parziale, target, t):
        #verificare che parziale sia possibile soluzioene
        #verificare se parziale è meglio di best
        #esci
        if len(parziale) == t+1:
            if self.getObjFun(parziale) > self._bestObjFun and parziale[-1] == target:
                self._bestPath = copy.deepcopy(parziale)
                self._bestObjFun = self.getObjFun(parziale)
            return


        #posso ancora aggiungere nodi : prendo i più vicini e provo ad aggiungere
        #ricorsione
        for n in self._grafo.neighbors(parziale[-1]):
            parziale.append(n)
            self.ricorsione(parziale, target, t)
            parziale.pop()


    def buildGraph(self, nMin):
        self._nodi = DAO.getALlNodes(nMin, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdgesV1()


    def getObjFun(self, listOfNodes):
        objVal = 0
        for i in range(0, len(listOfNodes)-1):
            objVal += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return objVal


    def _addEdgesV1(self):
        allConnessioni = DAO.getALlEdgesV1(self._idMap)
        for c in allConnessioni:
            v0 = c.v0
            v1 = c.v1
            peso = c.N

            if v0 in self._grafo and v1 in self._grafo:
                if self._grafo.has_edge(v0,v1):
                    self._grafo[v0][v1]["weight"] += peso

                else:
                    self._grafo.add_edge(v0,v1,weight=peso)

            """- Verifica dei Nodi: Viene controllato se entrambi i nodi v0 e v1 sono già presenti nel grafo (self._grafo).
                - Aggiornamento del Peso dell'Arco: Se esiste già un arco tra v0 e v1, il peso di quell'arco viene 
                  incrementato del valore peso.
                - Aggiunta di un Nuovo Arco: Se non esiste un arco tra v0 e v1, viene aggiunto un nuovo arco con il 
                  peso specificato peso"""

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)


    def getAllNodes(self):
        return self._nodi

    def getSortedVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTUple = []
        for v in vicini:
            viciniTUple.append((v, self._grafo[v0][v]["weight"]))

        viciniTUple.sort(key = lambda x:x[1], reverse = True)
        return viciniTUple


    def esistePercorso(self,v0,v1):
        connessa = nx.node_connected_component(self._grafo, v0)
        if v1 in connessa:
            return True
        else:
            return False


    def trovaCamminoV1(self, v0, v1):
        #diversi metodi
        #dijkstra
        return nx.dijkstra_path(self._grafo, v0, v1)  #restituisce lista di nodi. cammino ottimo

    def trovaCaminoV2(self, v0, v1):
        #costruisco albero di visita bfs o dfs
        tree = nx.bfs_tree(self._grafo, v0)  #restituisce grafo orientato con radice v0 e va verso le foglie

        #per recuperare il cammino
        path = [v1]
        while path[-1] != v0:
            path.append(list(tree.predecessors(path[-1]))[0]) #lo devo fare così perché predecessors mi restituisce un
            # iteratore
        path.reverse()
        return path


    def trovaCaminoV3(self, v0, v1):
        dfstree = nx.dfs_tree(self._grafo, v0)
        # per recuperare il cammino
        path = [v1]
        while path[-1] != v0:
            path.append(list(dfstree.predecessors(path[-1]))[0])  # lo devo fare così perché predecessors mi restituisce un
            # iteratore
        path.reverse()
        return path
