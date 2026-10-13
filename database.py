import os
import sqlite3

from graphFunctions import GRAPHS

#ensure database file is in same directory
current_directory = os.path.dirname(os.path.abspath(__file__))
DB_File = os.path.join(current_directory, "graphs.db")

def runCommandSql(sqlCommand, arguments = []):
    connection = sqlite3.connect(DB_File)
    try:
        cursor = connection.execute(sqlCommand, arguments)
        rows = cursor.fetchall()
        connection.commit()
        return rows
    finally:
        connection.close()

def initializeDatabase():
    runCommandSql(""" CREATE TABLE IF NOT EXISTS saved_graphs (
                            name VARCHAR(50) PRIMARY KEY,
                            function_name VARCHAR(20) NOT NULL,
                            parameters VARCHAR(50) NOT NULL) """)

def saveGraph(name, function_name, parameters):
    #convert all parameter values into comma seperated text. eg: "0.55,0.4", according to the order listed in GRAPHS

    strValuesInList = []
    for parameterName in GRAPHS[function_name]["parameters"]:
        value = parameters[parameterName]
        strValuesInList.append(str(value))
    parameterValuesText = ','.join(strValuesInList)

    #Saving graph under a name that already exists replaces it
    runCommandSql("INSERT OR REPLACE INTO saved_graphs (name, function_name, parameters) VALUES (?, ?, ?)", [name, function_name, parameterValuesText])

def listGraphs():
    #list all saved graphs sorted from newest to oldest

    rows = runCommandSql("SELECT name, function_name, parameters FROM saved_graphs ORDER BY rowid DESC")

    graphs = []
    for name, function_name, parametersText in rows:
        #convert comma seperated text back into parameter values like {"para_name":0.55, "para_name":0.4}, according to order of GRAPHS
        strValuesInList = parametersText.split(',')
        parameters = {}
        i = 0
        for parameterName in GRAPHS[function_name]["parameters"]:
            parameters[parameterName] = float(strValuesInList[i])
            i += 1

        graph = {"name" : name, "function_name" : function_name, "parameters" : parameters}
        graphs.append(graph)

    return graphs

def deleteGraph(name):
    runCommandSql("DELETE FROM saved_graphs WHERE name = ?", [name])

        
