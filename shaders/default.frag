#version 330 core

in vec3 fragPosition;
in vec2 fragTexCoord;
in vec3 fragNormal;

in vec3 cameraPosition;

uniform sampler2D albedoTexture;

layout(std140) uniform Material {
    vec3 ambient;
    vec3 albedo;
    vec3 specular;
    float a;
} mat;

vec3 phong(in vec3 N, in vec3 L, in vec3 V, in vec3 ambient, in vec3 diffuse, in vec3 specular, in float a) {
    vec3 R = reflect(-L, N);
    return ambient + max(dot(N, L),0.0) * diffuse + pow(max(dot(R, V),0.0), a) * specular;
}

void main() {
    vec3 N = normalize(fragNormal);
    vec3 lightPosition = vec3(10, 2, 5);
    vec3 L = normalize(lightPosition - fragPosition);
    vec3 V = normalize(cameraPosition - fragPosition);

    vec3 albedo = texture(albedoTexture, fragTexCoord).rgb;
    vec3 color = phong(N, L, V, 0.6 * vec3(pow(albedo.r, 4.0), pow(albedo.g, 4.0), pow(albedo.b, 4.0)),
    /* mat.albedo * */ albedo,
    vec3(pow(albedo.r, .5), pow(albedo.g, .5), pow(albedo.b, .5)), 50.0);

    gl_FragColor = vec4(color, 1.0);
    //gl_FragColor = vec4(texture(albedoTexture, fragTexCoord).rgb, 1.0);
    //gl_FragColor = vec4(N * 0.5 + 0.5, 1.0);
}