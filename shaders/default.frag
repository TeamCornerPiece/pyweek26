#version 330 core

in vec3 fragPosition;
in vec3 fragNormal;

void main() {
    float factor = dot(fragNormal, vec3(0, 0, -1)) * .3 + .7;
    gl_FragColor = vec4(factor, factor, factor, 1.0);
}