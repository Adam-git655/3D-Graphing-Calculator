from settings import *
import random
from metaball import MetaBall
from meshes.gridMesh import GridMesh
from meshes.triangleMesh import TriangleMesh
from lookupTable import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.metaballs = []
        self.numMetaballs = 5

        for i in range(0, self.numMetaballs):
            pos = glm.vec3(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                    )
            
            vel = glm.vec3(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                    )
            
            r = random.uniform(0.3, 0.7)
            
            mb = MetaBall(app, pos.x, pos.y, pos.z, vel.x, vel.y, vel.z, r)
            self.metaballs.append(mb)

        x = np.linspace(-BOUND, BOUND, GRID_SIZE + 1)
        y = np.linspace(-BOUND, BOUND, GRID_SIZE + 1)
        z = np.linspace(-BOUND, BOUND, GRID_SIZE + 1) 
        self.gridX, self.gridY, self.gridZ = np.meshgrid(x, y, z, indexing='ij')

        self.grid = GridMesh(app)
        self.triangleMesh = None

    def update(self):
        for ball in self.metaballs:
            ball.update()

        field = self.computeField()
        triangleSegs = self.marchCubes(field)

        if triangleSegs:
            self.triangleMesh = TriangleMesh(self.app, triangleSegs)
        else:
            self.triangleMesh = None

    def render(self):
        self.grid.render()
        # for ball in self.metaballs:
        #     ball.render()

        if self.triangleMesh:
            self.triangleMesh.render()

    def computeField(self):
        field = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1, GRID_SIZE + 1))
        for ball in self.metaballs:
            dx = self.gridX - ball.x
            dy = self.gridY - ball.y
            dz = self.gridZ - ball.z 
            field += ((ball.radius * ball.radius) / (dx * dx + dy * dy + dz * dz + 1e-5))
        return field
    
    def marchCubes(self, field):
        triangleSegments = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                for k in range(GRID_SIZE):

                    cornerFieldVals = np.array(
                        [
                            field[i, j, k],
                            field[i + 1, j, k],
                            field[i, j + 1, k],
                            field[i + 1, j + 1, k],
                            field[i, j, k + 1],
                            field[i + 1, j, k + 1],
                            field[i, j + 1, k + 1],
                            field[i + 1, j + 1, k + 1]
                        ]
                    )

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

                    bitIndex = ((cornerFieldVals[7] > 1.0) << 7 | 
                                (cornerFieldVals[6] > 1.0) << 6 | 
                                (cornerFieldVals[5] > 1.0) << 5 | 
                                (cornerFieldVals[4] > 1.0) << 4 |
                                (cornerFieldVals[3] > 1.0) << 3 |
                                (cornerFieldVals[2] > 1.0) << 2 |
                                (cornerFieldVals[1] > 1.0) << 1 |
                                (cornerFieldVals[0] > 1.0) << 0)
                    

                    edgeTriplets = LOOKUP_TRIANGLE_TABLE[bitIndex]

                    for t in range(0, len(edgeTriplets), 3):
                        if edgeTriplets[t] == -1:
                            break

                        p1 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t])
                        p2 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t + 1])
                        p3 = self.estimatePoint(cornerWorldPositions, cornerFieldVals, edgeTriplets[t + 2])
                        triangleSegments.append((p1, p2, p3))
        
        return triangleSegments
    
    def estimatePoint(self, cornerWorldPositions, cornerFieldVals, edge):
        vertices = EDGE_VERTEX_INDICES[edge]
        return  (
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][0], cornerWorldPositions[vertices[1]][0]),
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][1], cornerWorldPositions[vertices[1]][1]),
                    self.linearlyInterpolate(cornerFieldVals[vertices[0]], cornerFieldVals[vertices[1]], cornerWorldPositions[vertices[0]][2], cornerWorldPositions[vertices[1]][2])
                )   
    
    def linearlyInterpolate(self, fieldVal1, fieldVal2, point1, point2):
        return (point1 + (point2 - point1) * ((1 - fieldVal1)/(fieldVal2 - fieldVal1)))
                
                
        