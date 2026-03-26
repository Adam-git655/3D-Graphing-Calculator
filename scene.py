from settings import *
import random
import moderngl as mgl
from metaball import MetaBall
from meshes.gridMesh import GridMesh
from meshes.triangleMesh import TriangleMesh
from lookupTable import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.metaballs = []
        self.numMetaballs = 10

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

    def update(self):
        for ball in self.metaballs:
            ball.update()

        field = self.computeField()
        verts = self.marchCubes(field)

        if len(verts) > 0:
            data = np.array(verts, dtype="float32")
            self.commonMeshVBO.write(data.tobytes())
            self.vertexCount = len(verts)
        else:
            self.vertexCount = 0

    def render(self):
        # self.grid.render()
        # for ball in self.metaballs:
        #     ball.render()

        if self.vertexCount > 0:
            self.app.shader.triangle['time'].value = self.app.time
            self.commonMeshVAO.render(mgl.TRIANGLES, vertices=self.vertexCount)

    def computeField(self):
        field = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1, GRID_SIZE + 1))
        for ball in self.metaballs:
            dx = self.gridX - ball.x
            dy = self.gridY - ball.y
            dz = self.gridZ - ball.z 
            field += ((ball.radius * ball.radius) / (dx * dx + dy * dy + dz * dz + 1e-5))
        return field
    
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
            bitIndex |= ((cornerFieldValsFullGrid[bit] > 1.0).astype(np.int32) << bit)

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
        return (point1 + (point2 - point1) * ((1 - fieldVal1)/(fieldVal2 - fieldVal1)))
                
                
        