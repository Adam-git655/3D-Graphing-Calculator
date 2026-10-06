from settings import *
from meshes.baseMesh import BaseMesh
import moderngl as mgl

LETTER_STROKES = {
    'X': [((-0.5, -0.5), ( 0.5,  0.5)),
          ((-0.5,  0.5), ( 0.5, -0.5))],

    'Y': [((-0.5,  0.5), ( 0.0,  0.0)),
          (( 0.5,  0.5), ( 0.0,  0.0)),
          (( 0.0,  0.0), ( 0.0, -0.5))],

    'Z': [((-0.5,  0.5), ( 0.5,  0.5)),
          (( 0.5,  0.5), (-0.5, -0.5)),
          ((-0.5, -0.5), ( 0.5, -0.5))],
}

class GridMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.grid

        self.boxColor = (0.65, 0.65, 0.65, 1.0)
        self.gridColor = (0.75, 0.75, 0.75, 0.5)
        self.axesColor = (0.6, 0.6, 0.6, 1.0)
        self.letterColor = (0.4, 0.4, 0.4, 1.0)

        self.vboFormat = '3f 4f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()

    def addLetter(self, lines, letter, center, right, up, size):
        for stroke in LETTER_STROKES[letter]:
            (u1, v1), (u2, v2) = stroke
            u1 *= size
            v1 *= size
            u2 *= size
            v2 *= size

            x1 = center[0] + right[0] * u1 + up[0] * v1
            y1 = center[1] + right[1] * u1 + up[1] * v1
            z1 = center[2] + right[2] * u1 + up[2] * v1

            x2 = center[0] + right[0] * u2 + up[0] * v2
            y2 = center[1] + right[1] * u2 + up[1] * v2
            z2 = center[2] + right[2] * u2 + up[2] * v2

            lines += [(x1, y1, z1, *self.letterColor), (x2, y2, z2, *self.letterColor)]

              

    def getVertexData(self):
        lines = []

        #Draw bounding box
        # 4 edges along z
        lines += [(-BOUND, -BOUND, -BOUND, *self.boxColor), (-BOUND, -BOUND,  BOUND, *self.boxColor)]
        lines += [(-BOUND,  BOUND, -BOUND, *self.boxColor), (-BOUND,  BOUND,  BOUND, *self.boxColor)]
        lines += [( BOUND, -BOUND, -BOUND, *self.boxColor), ( BOUND, -BOUND,  BOUND, *self.boxColor)]
        lines += [( BOUND,  BOUND, -BOUND, *self.boxColor), ( BOUND,  BOUND,  BOUND, *self.boxColor)]

        # 4 edges along y
        lines += [(-BOUND, -BOUND, -BOUND, *self.boxColor), (-BOUND,  BOUND, -BOUND, *self.boxColor)]
        lines += [(-BOUND, -BOUND,  BOUND, *self.boxColor), (-BOUND,  BOUND,  BOUND, *self.boxColor)]
        lines += [( BOUND, -BOUND, -BOUND, *self.boxColor), ( BOUND,  BOUND, -BOUND, *self.boxColor)]
        lines += [( BOUND, -BOUND,  BOUND, *self.boxColor), ( BOUND,  BOUND,  BOUND, *self.boxColor)]

        # 4 edges along x
        lines += [(-BOUND, -BOUND, -BOUND, *self.boxColor), ( BOUND, -BOUND, -BOUND, *self.boxColor)]
        lines += [(-BOUND, -BOUND,  BOUND, *self.boxColor), ( BOUND, -BOUND,  BOUND, *self.boxColor)]
        lines += [(-BOUND,  BOUND, -BOUND, *self.boxColor), ( BOUND,  BOUND, -BOUND, *self.boxColor)]
        lines += [(-BOUND,  BOUND,  BOUND, *self.boxColor), ( BOUND,  BOUND,  BOUND, *self.boxColor)]

        #Draw grid lines at y = 0
        for i in np.arange(-BOUND, BOUND, .25):
                if i == 0:
                     continue
                
                lines += [(i, 0, -BOUND, *self.gridColor), (i, 0, BOUND, *self.gridColor)]
                lines += [(-BOUND, 0, i, *self.gridColor), (BOUND, 0, i, *self.gridColor)]

        #Draw coordinate axes
        arrowLength = 0.2
        arrowOffset = 0.08

        #X axes
        lines += [(-BOUND, 0, 0, *self.axesColor), (BOUND, 0, 0, *self.axesColor)]

        lines += [(BOUND, 0, 0, *self.axesColor), (BOUND - arrowLength, arrowOffset, 0, *self.axesColor)]
        lines += [(BOUND, 0, 0, *self.axesColor), (BOUND - arrowLength, -arrowOffset, 0, *self.axesColor)]
        lines += [(BOUND, 0, 0, *self.axesColor), (BOUND - arrowLength, 0, arrowOffset, *self.axesColor)]
        lines += [(BOUND, 0, 0, *self.axesColor), (BOUND - arrowLength, 0, -arrowOffset, *self.axesColor)]

        #Y axes
        lines += [(0, -BOUND, 0, *self.axesColor), (0, BOUND, 0, *self.axesColor)]

        lines += [(0, BOUND, 0, *self.axesColor), (arrowOffset, BOUND - arrowLength, 0, *self.axesColor)]
        lines += [(0, BOUND, 0, *self.axesColor), (-arrowOffset, BOUND - arrowLength, 0, *self.axesColor)]
        lines += [(0, BOUND, 0, *self.axesColor), (0, BOUND - arrowLength, arrowOffset, *self.axesColor)]
        lines += [(0, BOUND, 0, *self.axesColor), (0, BOUND - arrowLength, -arrowOffset, *self.axesColor)]

        #Z axes
        lines += [(0, 0, -BOUND, *self.axesColor), (0, 0, BOUND, *self.axesColor)]

        lines += [(0, 0, BOUND, *self.axesColor), (0, arrowOffset, BOUND - arrowLength, *self.axesColor)]
        lines += [(0, 0, BOUND, *self.axesColor), (0, -arrowOffset, BOUND - arrowLength, *self.axesColor)]
        lines += [(0, 0, BOUND, *self.axesColor), (arrowOffset, 0, BOUND - arrowLength, *self.axesColor)]
        lines += [(0, 0, BOUND, *self.axesColor), (-arrowOffset, 0, BOUND - arrowLength, *self.axesColor)]

        #Draw X, Y, Z letters in front of respective axes
        labelSize = 0.3
        gap = 0.5

        up = (0, 1, 0)

        self.addLetter(lines, 'X', (BOUND + gap, 0, 0), (1, 0, 0), up, labelSize)
        self.addLetter(lines, 'Y', (0, BOUND + gap, 0), (1, 0, 0), up, labelSize)
        self.addLetter(lines, 'Z', (0, 0, BOUND + gap), (0, 0, 1), up, labelSize)


        return np.array(lines, dtype="float32")
    
    def render(self):
        self.vao.render(mgl.LINES)
