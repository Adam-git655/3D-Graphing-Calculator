from settings import *

class Shader:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player
        self.cube = self.getShaderProgram(shader_name='cube')

        self.setUniformsOnInit()
        
    def setUniformsOnInit(self):
        self.cube['projMat'].write(self.player.projMat)
        self.cube['modelMat'].write(glm.mat4())

    def update(self):
        self.cube['viewMat'].write(self.player.viewMat)

    def getShaderProgram(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program