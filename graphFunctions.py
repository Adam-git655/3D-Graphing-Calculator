import numpy as np

def sphere(x, y, z, params):
    radius = params["radius"]
    return (x*x + y*y + z*z) - radius * radius

def torus(x, y, z, params):
    majorRadius = params["major_radius"]
    minorRadius = params["minor_radius"]

    return (np.sqrt(x*x + y*y) - majorRadius)**2 + z*z - minorRadius * minorRadius

def gyroid(x, y, z, params):
    a = np.pi * params["frequency"]
    return np.sin(x*a)*np.cos(y*a) + np.sin(y*a)*np.cos(z*a) + np.sin(z*a)*np.cos(x*a)



GRAPHS = {
    "sphere" : {
        "name" : "Sphere",
        "function" : sphere,
        "parameters" : {
            "radius" : {"default" : 0.4, "min":0.2, "max":0.95}
        }
    },

    "torus" : {
        "name" : "Torus",
        "function" : torus,
        "parameters" : {
            "major_radius" : {"default" : 0.55, "min" : 0.30, "max" : 0.65},
            "minor_radius" : {"default": 0.25, "min": 0.10, "max": 0.30}
        }
    },

    "gyroid" : {
        "name": "Gyroid",
        "function": gyroid,
        "parameters": {
            "frequency": {"default": 1.00, "min": 0.50, "max": 3.00},
        },
    },

    "metaballs" : {
        "name": "Metaballs",
        "function": None,
        "parameters": {
            "count": {"default": 10, "min": 2, "max": 20},
        },
    }
}

# The graphs Scene can draw from a function (everything except metaballs).
FUNCTIONS = {}
for key in GRAPHS:
    function = GRAPHS[key]["function"]
    if function is not None:
        FUNCTIONS[key] = function