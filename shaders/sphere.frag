#version 330 core

layout (location = 0) out vec4 fragColor;
in vec3 color;

void main()
{
    fragColor = vec4(fragColor, 1.0);
}