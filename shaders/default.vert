#version 330 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inNormal;

out vec3 fragPosition;
out vec3 fragNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main() {
    mat4 mvp = proj * view * model;
    gl_Position = mvp * vec4(inPosition, 1);
    fragNormal = transpose(inverse(mat3(model))) * inNormal;
}