#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 v_worldPos;
uniform float time;
uniform float bound;

void main()
{
    float t = (v_worldPos.y + bound) / (2.0 * bound);
    float r = 0.5 + 0.5 * sin(time + t * 3.14159);
    float g = 0.5 + 0.5 * sin(time + t * 3.14159 + 2.094);
    float b = 0.5 + 0.5 * sin(time + t * 3.14159 + 4.189);
    fragColor = vec4(0.5, 0.5, 0.5, 1.0);
}