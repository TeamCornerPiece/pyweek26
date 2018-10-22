#version 330 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec2 inTexCoord;
layout(location = 2) in vec3 inNormal;

out vec3 fragPosition;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec3 cameraPosition;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main() {
    mat4 mvp = proj * view * model;
    gl_Position = mvp * vec4(inPosition, 1.0);
    fragPosition = vec3(model * vec4(inPosition, 1.0));
    fragNormal = mat3(transpose(inverse(model))) * inNormal;
    fragTexCoord = inTexCoord;

    mat4 viewModel = view * model;
    mat4 modelView = inverse(viewModel);
    cameraPosition = vec3(inverse(view)[3]);
}