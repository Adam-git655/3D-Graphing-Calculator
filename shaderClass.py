from settings import *

class Shader:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player
        self.sphere = self.getShaderProgram(shader_name='sphere')
        self.grid = self.getShaderProgram(shader_name='grid')
        self.triangle = self.getShaderProgram(shader_name='triangle')

        self.setUniformsOnInit()
        
    def setUniformsOnInit(self):
        self.sphere['projMat'].write(self.player.projMat)
        self.sphere['modelMat'].write(glm.mat4())

        self.grid['projMat'].write(self.player.projMat)
        self.grid['modelMat'].write(glm.mat4())

        self.triangle['projMat'].write(self.player.projMat)
        self.triangle['modelMat'].write(glm.mat4())
        

    def update(self):
        self.sphere['viewMat'].write(self.player.viewMat)
        self.grid['viewMat'].write(self.player.viewMat)
        self.triangle['viewMat'].write(self.player.viewMat)

    def getShaderProgram(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program