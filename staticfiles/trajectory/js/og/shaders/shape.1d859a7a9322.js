/**
 * @module og/shaders/shape
 */

"use strict";

import { Program } from "../webgl/Program.js";
import { types } from "../webgl/types.js";

export function shape_wl() {
    return new Program("shape_wl", {
        uniforms: {
            viewMatrix: { type: types.MAT4 },
            projectionMatrix: { type: types.MAT4 },
            modelMatrix: { type: types.MAT4 },
            normalMatrix: { type: types.MAT4 },

            lightsPositions: { type: types.VEC4 },
            lightsParamsv: { type: types.VEC3 },
            lightsParamsf: { type: types.FLOAT },

            uColor: { type: types.VEC4 },
            uSampler: { type: types.SAMPLER2D }
        },
        attributes: {
            aVertexNormal: { type: types.VEC3 },
            aVertexPosition: { type: types.VEC3 },
            aTextureCoord: { type: types.VEC2 }
        },
        vertexShader: `attribute vec3 aVertexNormal;
            attribute vec3 aVertexPosition;
            attribute vec2 aTextureCoord;
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            uniform mat3 normalMatrix;
            varying vec2 vTextureCoord;
            varying vec3 vNormal;
            varying vec4 vPosition;

            void main(void) {
                vTextureCoord = aTextureCoord;
                vNormal = normalMatrix * aVertexNormal;
                vPosition = viewMatrix * modelMatrix * vec4(aVertexPosition, 1.0);
                gl_Position = projectionMatrix * vPosition;
            }`,
        fragmentShader: `precision highp float;
            varying vec2 vTextureCoord;
            varying vec3 vNormal;
            varying vec4 vPosition;
            uniform vec4 uColor;
            uniform sampler2D uSampler;
            #define MAX_POINT_LIGHTS 1
            uniform int lightsQuantity;
            uniform vec4 lightsPositions[MAX_POINT_LIGHTS];
            uniform vec3 lightsParamsv[MAX_POINT_LIGHTS * 3];
            uniform float lightsParamsf[MAX_POINT_LIGHTS];
            void main(void) {
                vec3 lightWeighting;
                vec3 lightDirection;
                vec3 normal;
                vec3 eyeDirection;
                vec3 reflectionDirection;
                float specularLightWeighting;
                float diffuseLightWeighting;
                lightDirection = normalize(lightsPositions[0].xyz - vPosition.xyz * lightsPositions[0].w);
                normal = normalize(vNormal);
                eyeDirection = normalize(-vPosition.xyz);
                reflectionDirection = reflect(-lightDirection, normal);
                specularLightWeighting = pow(max(dot(reflectionDirection, eyeDirection), 0.0), lightsParamsf[0]);
                diffuseLightWeighting = max(dot(normal, lightDirection), 0.0);
                lightWeighting = lightsParamsv[0] + lightsParamsv[1] * diffuseLightWeighting + lightsParamsv[2] * specularLightWeighting;
                vec4 cc = texture2D( uSampler, vTextureCoord.st );
                gl_FragColor = vec4(lightWeighting, uColor.a) * cc * uColor;
            }`
    });
}

export function shape_nl() {
    return new Program("shape_nl", {
        uniforms: {
            projectionViewMatrix: { type: types.MAT4 },
            modelMatrix: { type: types.MAT4 },
            uColor: { type: types.VEC4 },
            uSampler: { type: types.SAMPLER2D }
        },
        attributes: {
            aVertexPosition: { type: types.VEC3, enableArray: true },
            aTextureCoord: { type: types.VEC2, enableArray: true }
        },
        vertexShader: `attribute vec3 aVertexPosition;
            attribute vec2 aTextureCoord;
            uniform mat4 projectionViewMatrix;
            uniform mat4 modelMatrix;
            varying vec2 vTextureCoord;

            void main(void) {
                gl_Position = projectionViewMatrix * (modelMatrix * vec4(aVertexPosition, 1.0));
                vTextureCoord = aTextureCoord;
            }`,
        fragmentShader: `precision highp float;
            uniform vec4 uColor;
            uniform sampler2D uSampler;
            varying vec2 vTextureCoord;
            void main(void) {
                gl_FragColor = uColor*texture2D( uSampler, vTextureCoord.st );
            }`
    });
}

export function shape_picking() {
    return new Program("shape_picking", {
        uniforms: {
            projectionViewMatrix: { type: types.MAT4 },
            modelMatrix: { type: types.MAT4 },
            uColor: { type: types.VEC4 }
        },
        attributes: {
            aVertexPosition: { type: types.VEC3, enableArray: true }
        },
        vertexShader: `attribute vec3 aVertexPosition;
            uniform mat4 projectionViewMatrix;
            uniform mat4 modelMatrix;

            void main(void) {
                gl_Position = projectionViewMatrix * (modelMatrix * vec4(aVertexPosition, 1.0));
            }`,
        fragmentShader: `precision highp float;
            uniform vec4 uColor;
            uniform sampler2D uSampler;
            void main(void) {
                gl_FragColor = uColor;
            }`
    });
}
