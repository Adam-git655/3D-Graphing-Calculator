from settings import *
import random
import moderngl as mgl
from metaball import MetaBall
from meshes.gridMesh import GridMesh
from meshes.triangleMesh import TriangleMesh
from lookupTable import *
from graphFunctions import FUNCTIONS

class Scene:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.metaballs = []

        self.graphKey = None
        self.graphValues = {}

        x = np.linspace(-BOUND, BOUND, GRID_SIZE + 1)
        y = np.linspace(-BOUND, BOUND, GRID_SIZE + 1)
        z = np.linspace(-BOUND, BOUND, GRID_SIZE + 1) 
        self.gridX, self.gridY, self.gridZ = np.meshgrid(x, y, z, indexing='ij')

        self.grid = GridMesh(app)
        self.showGrid = True
        self.triangleMesh = None
        self.updateField = True

        MAX_TRIANGLES = GRID_SIZE ** 3 * 5
        MAX_VERTICES = MAX_TRIANGLES * 3

        self.commonMeshVBO = self.ctx.buffer(
            reserve = MAX_VERTICES * 3 * 4,  #total bytes to prereserve on gpu
            dynamic = True #fast writes
        )

        self.commonMeshVAO = self.ctx.vertex_array(
            self.app.shader.triangle,
            [(self.commonMeshVBO, '3f', 'in_position')],
            skip_errors = True
        )

        self.vertexCount = 0

    def setGraph(self, key, values):
        self.graphKey = key
        self.graphValues = dict(values)
        self.metaballs = []

        if key == "metaballs":
            numMetaballs = int(round(values["count"]))
            for i in range(numMetaballs):
                x = random.uniform(-1, 1)
                y = random.uniform(-1, 1)
                z = random.uniform(-1, 1)
                velX = random.uniform(-1, 1)
                velY = random.uniform(-1, 1)
                velZ = random.uniform(-1, 1)
                radius = random.uniform(0.3, 0.7)

                mb = MetaBall(self.app, x, y, z, velX, velY, velZ, radius)
                self.metaballs.append(mb)

        self.updateField = True


    def update(self):
        if (self.graphKey is None):
            return

        #keep updating field for metaballs since its an animated function. dont do that for static functions
        if (self.graphKey == "metaballs"):
            for ball in self.metaballs:
                ball.update()
        elif self.updateField == "False":
            return

        self.updateField = False

        field = self.computeField()
        verts = self.marchCubes(field)

        if len(verts) > 0:
            data = np.array(verts, dtype="float32")
            self.commonMeshVBO.write(data.tobytes())
            self.vertexCount = len(verts)
        else:
            self.vertexCount = 0

    def render(self):
        if self.showGrid:
            self.grid.render()
            
        if self.vertexCount > 0:
            self.app.shader.triangle['time'].value = self.app.time
            self.commonMeshVAO.render(mgl.TRIANGLES, vertices=self.vertexCount)

    def computeField(self):
        x, y, z = self.gridX, self.gridY, self.gridZ

        #metaballs
        if (self.graphKey == "metaballs"):
            field = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1, GRID_SIZE + 1))
            for ball in self.metaballs:
                dx = x - ball.x
                dy = y - ball.y
                dz = z - ball.z 
                field += ((ball.radius * ball.radius) / (dx * dx + dy * dy + dz * dz + 1e-5))
            field -= 1
            return field
        #static functions
        else:
            function = FUNCTIONS[self.graphKey]
            #convert global coordinates (-B to B) into box coordinates (-1 to 1), for the function
            boxX = x / BOUND
            boxY = y / BOUND
            boxZ = z / BOUND
            return function(boxX, boxY, boxZ, self.graphValues)
    
    def marchCubes(self, field):
        verts = []

        cornerFieldValsFullGrid = [
            field[:-1, :-1, :-1],
            field[1:, :-1, :-1],
            field[:-1, 1:, :-1],
            field[1:, 1:, :-1],
            field[:-1, :-1, 1:],
            field[1:, :-1, 1:],
            field[:-1, 1:, 1:],
            field[1:, 1:, 1:]
        ]

        bitIndex = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=np.int32)
        for bit in range(8):
            bitIndex |= ((cornerFieldValsFullGrid[bit] > ISO_LEVEL).astype(np.int32) << bit)

        activeCells = np.argwhere((bitIndex > 0) & (bitIndex < 255))

        for (i, j, k) in activeCells:
            bitIdx = bitIndex[i, j, k]
            cornerFieldVals = np.array([cornerFieldValsFullGrid[b][i, j, k] for b in range(8)])

            cornerWorldPositions = np.array(
                [
                    (self.gridX[i, j, k], self.gridY[i, j, k], self.gridZ[i, j, k]),
                    (self.gridX[i + 1, j, k], self.gridY[i + 1, j, k], self.gridZ[i + 1, j, k]),
                    (self.gridX[i, j + 1, k], self.gridY[i, j + 1, k], self.gridZ[i, j + 1, k]),
                    (self.gridX[i + 1, j + 1, k], self.gridY[i + 1, j + 1, k], self.gridZ[i + 1, j + 1, k]),
                    (self.gridX[i, j, k + 1], self.gridY[i, j, k + 1], self.gridZ[i, j, k + 1]),
                    (self.gridX[i + 1, j, k + 1], self.gridY[i + 1, j, k + 1], self.gridZ[i + 1, j, k + 1]),
                    (self.gridX[i, j + 1, k + 1], self.gridY[i, j + 1, k + 1], self.gridZ[i, j + 1, k + 1]),
                    (self.gridX[i + 1, j + 1, k + 1], self.gridY[i + 1, j + 1, k + 1], self.gridZ[i + 1, j + 1, k + 1])
                ]
            )

            edgeTriplets = LOOKUP_TRIANGLE_TABLE[bitIdx]

            for t in range(0, len(edgeTriplets), 3):
                if edgeTriplets[t] == -1:
                    break

                p1 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t])
                p2 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t + 1])
                p3 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t + 2])
                verts.extend([p1, p2, p3])
        
        return verts
    
    def estimatePoint(self, cornerWorldPositions, cornerFieldVals, edge):
        vertices = EDGE_VERTEX_INDICES[edge]
        return  (
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][0], cornerWorldPositions[vertices[1]][0]),
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][1], cornerWorldPositions[vertices[1]][1]),
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][2], cornerWorldPositions[vertices[1]][2])
                )   
    
    def linearlyInterpolate(self, fieldVal1, fieldVal2, point1, point2):
        return (point1 + (point2 - point1) * ((ISO_LEVEL - fieldVal1)/(fieldVal2 - fieldVal1)))
                
                
        