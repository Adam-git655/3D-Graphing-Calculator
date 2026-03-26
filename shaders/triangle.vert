#version 330 core

layout (location = 0) in vec3 in_position;

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

out vec3 v_worldPos;

void main()
{
    v_worldPos = in_position;
    gl_Position = projMat * viewMat * modelMat * vec4(in_position, 1.0);
}