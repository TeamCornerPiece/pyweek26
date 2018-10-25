#version 330 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec2 inTexCoord;
layout(location = 2) in vec3 inNormal;

uniform float time;

out vec3 fragPosition;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec3 cameraPosition;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main() {
    mat4 mvp = proj * view * model;
    vec3 position = inPosition;

    position.y += 2.0 * (sin(position.x * radians(360.0) * 2.0 + time) * 0.5 + 0.5);
	gl_Position = mvp * vec4(position, 1.0);

    fragPosition = vec3(model * vec4(position, 1.0));
    fragNormal = mat3(transpose(inverse(model))) * inNormal;
    fragTexCoord = inTexCoord;

    cameraPosition = vec3(inverse(view)[3]);
}
