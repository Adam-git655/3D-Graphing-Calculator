from settings import *
from meshes.baseMesh import BaseMesh

class SphereMesh(BaseMesh):
    def __init__(self, app, latitudes=20, longitudes=20, r=0.5):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.sphere

        self.totalLats = latitudes
        self.totalLongs = longitudes
        self.r = r

        self.vboFormat = '3f 3f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()


    def getVertexData(self):
        globe = {}
        for i in range(self.totalLats + 1):
            lat = np.pi * i / self.totalLats
            for j in range(self.totalLongs + 1):
                long = 2 * np.pi * j / self.totalLongs
                x = self.r * np.sin(lat) * np.cos(long)
                y = self.r * np.cos(lat)
                z = self.r * np.sin(lat) * np.sin(long)
                globe[i, j] = (x, y, z)
        
        vertices = []
        colors = []

        for i in range(self.totalLats):
            for j in range(self.totalLongs):
                tl = globe[i, j]
                tr = globe[i, j + 1]
                bl = globe[i + 1, j]
                br = globe[i + 1, j + 1]

                vertices += [tl, tr, br,  tl, br, bl]

                t = i / self.totalLats
                colors += [(1-t, 0.3, t)] * 6
            

        return np.hstack([
            np.array(vertices, dtype="float32"),
            np.array(colors, dtype="float32")
        ])
