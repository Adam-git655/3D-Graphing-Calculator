#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

out vec3 color;

void main()
{
    color = in_color;
    gl_Position = projMat * viewMat * modelMat * vec4(in_position, 1.0);
}