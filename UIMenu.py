import sqlite3
from imgui_bundle import imgui
import database
from graphFunctions import GRAPHS

class UIMenu:
    def __init__(self, scene):
        self.scene = scene

        self.functionKeys = []
        self.functionNames = []
        for key in GRAPHS:
            self.functionKeys.append(key)
            self.functionNames.append(GRAPHS[key]["name"])

        self.selectedFunctionIndex = 0
        self.values = {} #current value of each parameter of function (for slider)

        #saving parameters
        self.saveName = ""
        self.savedGraphs = []
        self.selectedSavedGraphIndex = -1
        self.statusMessage = ""

        database.initializeDatabase() #create saved_graphs table if not exists
        self.refreshSavedGraphs()
        self.chooseFunction(0)

    def getDefaultParametersOfFunction(self, key):
        defaults = {}
        for parameterName in GRAPHS[key]["parameters"]:
            limits = GRAPHS[key]["parameters"][parameterName]
            defaults[parameterName] = limits["default"]
        return defaults

    def chooseFunction(self, index):
        self.selectedFunctionIndex = index
        self.values = self.getDefaultParametersOfFunction(self.functionKeys[index])
        self.applyGraph()

    def applyGraph(self):
        self.scene.setGraph(self.functionKeys[self.selectedFunctionIndex], self.values)

    def saveCurrentGraph(self):
        name = self.saveName.strip()
        if name == "":
            self.statusMessage = "Type a name first before saving"
            return

        key = self.functionKeys[self.selectedFunctionIndex]
        try:
            database.saveGraph(name, key, self.values)
            self.refreshSavedGraphs()
        except sqlite3.Error as error:
            self.statusMessage = "Database error: " + str(error)
            return
        
        self.statusMessage = "Saved '" + name + "'"

    def refreshSavedGraphs(self):
        self.savedGraphs = database.listGraphs()
        self.selectedSavedGraphIndex = -1

    def loadSelectedGraph(self):
        if self.selectedSavedGraphIndex < 0:
            self.statusMessage = "Click a saved graph in the list first."
            return

        graph = self.savedGraphs[self.selectedSavedGraphIndex]

        for i in range(len(self.functionKeys)):
            if self.functionKeys[i] == graph["function_name"]:
                self.selectedFunctionIndex = i

        self.values = dict(graph["parameters"])
        self.applyGraph()  
        self.statusMessage = "Loaded: '" + graph["name"] + "'"

    def deleteSelectedGraph(self):
        if self.selectedSavedGraphIndex < 0:
            self.statusMessage = "Click a saved graph in the list first."
            return

        name = self.savedGraphs[self.selectedSavedGraphIndex]["name"]
        try:
            database.deleteGraph(name)
            self.refreshSavedGraphs()
        except sqlite3.Error as error:
            self.statusMessage = "Database error: " + str(error)
            return
        self.statusMessage = "Deleted '" + name + "'"

    def draw(self):
        imgui.set_next_window_pos(imgui.ImVec2(0, 0), imgui.Cond_.first_use_ever)
        imgui.set_next_window_size(imgui.ImVec2(340, 0), imgui.Cond_.first_use_ever)
        imgui.begin("GraphMenu")

        #function choosing dropdown
        result = imgui.combo("Function", self.selectedFunctionIndex, self.functionNames)

        functionChanged = result[0]
        newIndex = result[1]
        if functionChanged:
            self.chooseFunction(newIndex)

        #sliders for function parameters
        imgui.text("Release a slider to redraw function")
        key = self.functionKeys[self.selectedFunctionIndex]
        for parameterName in GRAPHS[key]["parameters"]:
            limits = GRAPHS[key]["parameters"][parameterName]
            label = parameterName.replace("_", " ")

            if isinstance(limits["default"], int):
                currentVal = int(round(self.values[parameterName]))
                result = imgui.slider_int(label, currentVal, limits["min"], limits["max"])
            else:
                currentVal = float(self.values[parameterName])
                result = imgui.slider_float(label, currentVal, limits["min"], limits["max"])

            sliderMoved = result[0]
            if sliderMoved:
                self.values[parameterName] = round(result[1], 3)

            if imgui.is_item_deactivated_after_edit():
                self.applyGraph()

        #Saving
        imgui.separator()
        imgui.text("Save the current graph")
        result = imgui.input_text("Name", self.saveName)
        self.saveName = result[1]
        if imgui.button("Save"):
            self.saveCurrentGraph()

        #saved graphs
        imgui.separator()
        imgui.text("Saved graphs")
        if imgui.begin_list_box("##savedGraphs", imgui.ImVec2(-1, 110)):
            for i in range(len(self.savedGraphs)):
                graph = self.savedGraphs[i]
                label = graph["name"] + "  (" + graph["function_name"] + ")" + "##" + str(i)

                if (i == self.selectedSavedGraphIndex):
                    isSelected = True
                else:
                    isSelected = False

                result = imgui.selectable(label, isSelected)
                if (result[0]):
                    self.selectedSavedGraphIndex = i

            imgui.end_list_box()

        if imgui.button("Load"):
            self.loadSelectedGraph()
        imgui.same_line()
        if imgui.button("Delete"):
            self.deleteSelectedGraph()

        imgui.text_wrapped(self.statusMessage)

        imgui.end()