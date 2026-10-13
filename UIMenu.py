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

    def draw(self):
        imgui.set_next_window_size(imgui.ImVec2(340, 300), imgui.Cond_.first_use_ever)
        imgui.begin("GraphMenu")
        imgui.end()