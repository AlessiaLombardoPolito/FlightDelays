import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAereoportoA = None
        self._choiceAereoportoP = None

    def handleAnalizza(self, e):
        nMinstr = self._view.txt_name.value
        try:
            nMin = int(nMinstr)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Il valore inserito nel campo non è un intero"))
            self._view._page.update()
            return

        self._model.buildGraph(nMin)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi : {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi : {self._model.getNumArchi()}"))
        self.fillDD()
        self._view._page.update()





    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view._ddAereoportoP.options.append(ft.dropdown.Option(
                data = n,
                on_click= self.readDDaeroportoP,
                text = n.AIRPORT
            ))
            self._view._ddAereoportoA.options.append(ft.dropdown.Option(
                data=n,
                on_click= self.readDDaeroportoA,
                text=n.AIRPORT
            ))


    def readDDaeroportoP(self,e):
        if e.control.data is None:
            self._choiceAereoportoP = None
        else:
            self._choiceAereoportoP = e.control.data

    def readDDaeroportoA(self,e):
        if e.control.data is None:
            self._choiceAereoportoA = None
        else:
            self._choiceAereoportoA = e.control.data




    def handleConnessi(self, e):
        if self._choiceAereoportoP is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza"))
            return

        v0 = self._choiceAereoportoP
        vicini = self._model.getSortedVicini(v0)
        self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view._page.update()


    def handleTestConnessione(self,e):
        v0 = self._choiceAereoportoP
        v1 = self._choiceAereoportoA

        #verificare che ci sia un percorso

        if (not self._model.esistePercorso(v0,v1)):
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {v0} e {v1}"))
            self._view._page.update()

            return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Esiste un percorso tra {v0} e {v1}"))
            dijkstra = self._model.trovaCamminoV1(v0,v1)
            BFS = self._model.trovaCaminoV2(v0, v1)
            DFS = self._model.trovaCaminoV3(v0, v1)
            self._view.txt_result.controls.append(ft.Text(f"Il percorso trovato con il metodo di dijkstra è :"))
            for p in dijkstra:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))
            self._view.txt_result.controls.append(ft.Text(f"    "))

            self._view.txt_result.controls.append(ft.Text(f"Il percorso trovato con il metodo di BFS è : "))
            for p in BFS:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))
            self._view.txt_result.controls.append(ft.Text(f"    "))

            self._view.txt_result.controls.append(ft.Text(f"Il percorso trovato con il metodo di DFS è : "))
            for p in DFS:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))

            self._view._page.update()


    def handleItinerario(self, e):
        global tInt
        v0 = self._choiceAereoportoP
        v1 = self._choiceAereoportoA
        t = self._view._txtInNumTratte.value

        try :
            tInt = int(t)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Il valore inserito non è un numero intero"))
        path = self._model.camminoOttimo(v0, v1, tInt)
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text(f"Il percorso ottimo tra {v0} e {v1} è :"))
        for p in path[0]:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Il peso è: {path[1]}"))

        self._view._page.update()






