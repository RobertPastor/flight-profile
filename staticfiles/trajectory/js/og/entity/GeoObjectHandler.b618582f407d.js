"use strict";

/**
 * @module og/entity/ShapeHandler
 */
import * as shaders from "../shaders/geoObject.js";
import { concatArrays, makeArrayTyped, spliceArray } from "../utils/shared.js";

const VERTEX_BUFFER = 0,
    POSITION_BUFFER = 1,
    RGBA_BUFFER = 2,
    NORMALS_BUFFER = 3,
    INDECIES_BUFFER = 4,
    DIRECTION_BUFFER = 5,
    PITCH_ROLL_BUFFER = 6,
    SIZE_BUFFER = 7,
    PICKINGCOLOR_BUFFER = 8,
    VISIBLE_BUFFER = 9;

const setParametersToArray = (arr = [], index = 0, length, itemSize, ...params) => {
    const currIndex = index * length;
    for (let i = currIndex, len = currIndex + length; i < len; i++) {
        arr[i] = params[i % itemSize];
    }
    return arr;
};

class GeoObjectHandler {
    constructor(entityCollection) {
        /**
         * Picking rendering option.
         * @public
         * @type {boolean}
         */
        this.pickingEnabled = true;

        this._entityCollection = entityCollection;
        this._renderer = null;
        this._planet = null;

        this._geoObjects = [];
        this._pitchRollArr = [[]];
        this._sizeArr = [[]];
        this._vertexArr = [[]];
        this._positionHighArr = [[]];
        this._positionLowArr = [[]];
        this._directionArr = [[]];
        this._rgbaArr = [[]];
        this._normalsArr = [[]];
        this._indicesArr = [[]];
        this._pickingColorArr = [[]];
        this._vehicleVisibleArr = [[]];

        this._pitchRollBuffer = [];
        this._sizeBuffer = [];
        this._vertexBuffer = [];
        this._positionHighBuffer = [];
        this._positionLowBuffer = [];
        this._directionBuffer = [];
        this._rgbaBuffer = [];
        this._normalsBuffer = [];
        this._indicesBuffer = [];
        this._pickingColorBuffer = [];
        this._vehicleVisibleBuffer = [];

        this.__staticId = GeoObjectHandler._staticCounter++;
        this._buffersUpdateCallbacks = [];
        this._buffersUpdateCallbacks[PICKINGCOLOR_BUFFER] = this.createPickingColorBuffer;
        this._buffersUpdateCallbacks[POSITION_BUFFER] = this.createPositionBuffer;
        this._buffersUpdateCallbacks[DIRECTION_BUFFER] = this.createDirectionBuffer;
        this._buffersUpdateCallbacks[NORMALS_BUFFER] = this.createNormalsBuffer;
        this._buffersUpdateCallbacks[RGBA_BUFFER] = this.createRgbaBuffer;
        this._buffersUpdateCallbacks[INDECIES_BUFFER] = this.createIndicesBuffer;
        this._buffersUpdateCallbacks[VERTEX_BUFFER] = this.createVertexBuffer;
        this._buffersUpdateCallbacks[SIZE_BUFFER] = this.createSizeBuffer;
        this._buffersUpdateCallbacks[PITCH_ROLL_BUFFER] = this.createPitchRollBuffer;
        this._buffersUpdateCallbacks[VISIBLE_BUFFER] = this.createVisibleBuffer;

        this._changedBuffers = new Array(this._buffersUpdateCallbacks.length);

        this._instancedTags = new Map();
    }

    getObjectByIndex(index) {
        return this._geoObjects[index];
    }

    //Create buffers
    createVertexBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._vertexArr.length; i < len; i++) {
            this._vertexBuffer && h.gl.deleteBuffer(this._vertexBuffer[i]);
            this._vertexArr[i] = makeArrayTyped(this._vertexArr[i]);
            this._vertexBuffer[i] = h.createArrayBuffer(this._vertexArr[i], 3, this._vertexArr[i].length / 3);
        }
    }

    createPitchRollBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._pitchRollArr.length; i < len; i++) {
            this._pitchRollBuffer && h.gl.deleteBuffer(this._pitchRollBuffer[i]);
            this._pitchRollArr[i] = makeArrayTyped(this._pitchRollArr[i]);
            this._pitchRollBuffer[i] = h.createArrayBuffer(this._pitchRollArr[i], 2, this._pitchRollArr[i].length / 2);
        }
    }

    createVisibleBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._vehicleVisibleArr.length; i < len; i++) {
            this._vehicleVisibleBuffer && h.gl.deleteBuffer(this._vehicleVisibleBuffer[i]);
            this._vehicleVisibleArr[i] = makeArrayTyped(this._vehicleVisibleArr[i]);
            this._vehicleVisibleBuffer[i] = h.createArrayBuffer(this._vehicleVisibleArr[i], 1, this._vehicleVisibleArr[i].length);
        }
    }

    createSizeBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._sizeArr.length; i < len; i++) {
            this._sizeBuffer && h.gl.deleteBuffer(this._sizeBuffer[i]);
            this._sizeArr[i] = makeArrayTyped(this._sizeArr[i]);
            this._sizeBuffer[i] = h.createArrayBuffer(this._sizeArr[i], 1, this._sizeArr[i].length);
        }
    }

    createPositionBuffer() {
        let h = this._renderer.handler;
        for (let i = 0, len = this._positionHighArr.length; i < len; i++) {
            this._positionHighBuffer && h.gl.deleteBuffer(this._positionHighBuffer[i]);
            this._positionHighArr[i] = makeArrayTyped(this._positionHighArr[i]);
            this._positionHighBuffer[i] = h.createArrayBuffer(this._positionHighArr[i], 3, this._positionHighArr[i].length / 3);
            this._positionLowBuffer && h.gl.deleteBuffer(this._positionLowBuffer[i]);
            this._positionLowArr[i] = makeArrayTyped(this._positionLowArr[i]);
            this._positionLowBuffer[i] = h.createArrayBuffer(this._positionLowArr[i], 3, this._positionLowArr[i].length / 3);
        }
    }

    createRgbaBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._rgbaArr.length; i < len; i++) {
            this._rgbaBuffer && h.gl.deleteBuffer(this._rgbaBuffer[i]);
            this._rgbaArr[i] = makeArrayTyped(this._rgbaArr[i]);
            this._rgbaBuffer[i] = h.createArrayBuffer(this._rgbaArr[i], 4, this._rgbaArr[i].length / 4);
        }
    }

    createDirectionBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._directionArr.length; i < len; i++) {
            this._directionBuffer && h.gl.deleteBuffer(this._directionBuffer[i]);
            this._directionArr[i] = makeArrayTyped(this._directionArr[i]);
            this._directionBuffer[i] = h.createArrayBuffer(this._directionArr[i], 3, this._directionArr[i].length / 3);
        }
    }

    createNormalsBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._normalsArr.length; i < len; i++) {
            this._normalsBuffer && h.gl.deleteBuffer(this._normalsBuffer[i]);
            this._normalsArr[i] = makeArrayTyped(this._normalsArr[i]);
            this._normalsBuffer[i] = h.createArrayBuffer(this._normalsArr[i], 3, this._normalsArr[i].length / 3);
        }
    }

    createIndicesBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._indicesArr.length; i < len; i++) {
            this._indicesBuffer && h.gl.deleteBuffer(this._indicesBuffer[i]);
            this._indicesArr[i] = makeArrayTyped(this._indicesArr[i], Uint16Array);
            this._indicesBuffer[i] = h.createElementArrayBuffer(this._indicesArr[i], 1, this._indicesArr[i].length);
        }
    }

    createPickingColorBuffer() {
        const h = this._renderer.handler;
        for (let i = 0, len = this._pickingColorArr.length; i < len; i++) {
            this._pickingColorBuffer && h.gl.deleteBuffer(this._pickingColorBuffer[i]);
            this._pickingColorArr[i] = makeArrayTyped(this._pickingColorArr[i]);
            this._pickingColorBuffer[i] = h.createArrayBuffer(this._pickingColorArr[i], 3, this._pickingColorArr[i].length / 3);
        }
    }

    static get _staticCounter() {
        if (!this._counter && this._counter !== 0) {
            this._counter = 0;
        }
        return this._counter;
    }

    static set _staticCounter(n) {
        this._counter = n;
    }

    initProgram() {
        if (this._renderer.handler) {
            if (!this._renderer.handler.programs.geo_object) {
                this._renderer.handler.addProgram(shaders.geo_object());
            }
            if (!this._renderer.handler.programs.geo_object_picking) {
                this._renderer.handler.addProgram(shaders.geo_object_picking());
            }
        }
    }

    setRenderNode(renderNode) {
        this._renderer = renderNode.renderer;
        this._planet = renderNode;
        this.initProgram();
    }

    setRenderer(planet) {
        super.setRenderer(planet);
    }

    _addGeoObjectToArray(geoObject) {
        let itemSize = 3;

        const tag = geoObject.tag,
            alreadyAdded = this._instancedTags.has(tag);

        if (!alreadyAdded) {
            this._instancedTags.set(tag, {
                iCounts: 1,
                maxIndex: Math.max(...geoObject._indices),
                index: this._instancedTags.size
            });
        } else {
            const prevState = this._instancedTags.get(tag),
                nextCount = prevState.iCounts + 1;
            this._instancedTags.set(tag, {
                ...prevState,
                iCounts: nextCount
            });
        }
        const tagData = this._instancedTags.get(tag),
            ti = tagData.index;

        /**
         * mark object by index for recalc indices array
         */
        geoObject._tagIndex = tagData.iCounts - 1;

            if (!this._vertexArr[ti] || this._vertexArr[ti].length !== geoObject._vertices.length) {

                this._vertexArr[ti] = concatArrays(
                    this._vertexArr[ti],
                    setParametersToArray(
                        [],
                        0,
                        geoObject._verticesCount * itemSize,
                        geoObject._verticesCount * itemSize,
                        ...geoObject._vertices
                    )
                );
                this._normalsArr[ti] = concatArrays(
                    this._normalsArr[ti],
                    setParametersToArray(
                        [],
                        0,
                        geoObject._verticesCount * itemSize,
                        geoObject._verticesCount * itemSize,
                        ...geoObject._normals
                        // ...getTriangleNormals(geoObject._vertices, geoObject._indices)
                    )
                );
            }
        this._vehicleVisibleArr[ti] = concatArrays(
            this._vehicleVisibleArr[ti],
            setParametersToArray([], 0, 1, 1, geoObject._visibility ? 1 : 0)
        );

        let x = geoObject._positionHigh.x,
            y = geoObject._positionHigh.y,
            z = geoObject._positionHigh.z,
            w;

        this._positionHighArr[ti] = concatArrays(
            this._positionHighArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y, z)
        );
        x = geoObject._positionLow.x;
        y = geoObject._positionLow.y;
        z = geoObject._positionLow.z;
        this._positionLowArr[ti] = concatArrays(
            this._positionLowArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y, z)
        );

        x = geoObject._entity._pickingColor.x / 255;
        y = geoObject._entity._pickingColor.y / 255;
        z = geoObject._entity._pickingColor.z / 255;
        this._pickingColorArr[ti] = concatArrays(
            this._pickingColorArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y, z)
        );

        x = geoObject._direction.x;
        y = geoObject._direction.y;
        z = geoObject._direction.z;
        this._directionArr[ti] = concatArrays(
            this._directionArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y, z)
        );

        itemSize = 4;

        x = geoObject._color.x;
        y = geoObject._color.y;
        z = geoObject._color.z;
        w = geoObject._color.w;
        this._rgbaArr[ti] = concatArrays(
            this._rgbaArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y, z, w)
        );

        x = geoObject._pitch;
        y = geoObject._roll;

        itemSize = 2;

        this._pitchRollArr[ti] = concatArrays(
            this._pitchRollArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, x, y)
        );

        itemSize = 1;

        this._sizeArr[ti] = concatArrays(
            this._sizeArr[ti],
            setParametersToArray([], 0, itemSize, itemSize, geoObject.scale)
        );
        this._addIndices(geoObject);
    }

    _displayPASS() {
        const r = this._renderer,
            sh = r.handler.programs.geo_object,
            p = sh._program,
            u = p.uniforms,
            a = p.attributes,
            gl = r.handler.gl,
            ec = this._entityCollection;

        sh.activate();

        gl.enable(gl.CULL_FACE);
        gl.uniform3fv(u.uScaleByDistance, ec.scaleByDistance);

        gl.uniform3fv(u.eyePositionHigh, r.activeCamera.eyeHigh);
        gl.uniform3fv(u.eyePositionLow, r.activeCamera.eyeLow);

        gl.uniformMatrix4fv(u.projectionMatrix, false, r.activeCamera.getProjectionMatrix());
        gl.uniformMatrix4fv(u.viewMatrix, false, r.activeCamera.getViewMatrix());
        gl.uniformMatrix3fv(u.normalMatrix, false, r.activeCamera._normalMatrix._m);

        gl.uniform4fv(u.lightsPositions, this._planet._lightsTransformedPositions);
        gl.uniform3fv(u.lightsParamsv, this._planet._lightsParamsv);
        gl.uniform1fv(u.lightsParamsf, this._planet._lightsParamsf);

        for (const tag of this._instancedTags) {
            const tagData = tag[1],
                ti = tagData.index;

            gl.bindBuffer(gl.ARRAY_BUFFER, this._normalsBuffer[ti]);
            gl.vertexAttribPointer(a.aVertexNormal, this._normalsBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._vertexBuffer[ti]);
            gl.vertexAttribPointer(a.aVertexPosition, this._vertexBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._directionBuffer[ti]);
            gl.vertexAttribPointer(a.aDirection, this._directionBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._sizeBuffer[ti]);
            gl.vertexAttribPointer(a.aScale, this._sizeBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._pitchRollBuffer[ti]);
            gl.vertexAttribPointer(a.aPitchRoll, this._pitchRollBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._rgbaBuffer[ti]);
            gl.vertexAttribPointer(a.aColor, this._rgbaBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._vehicleVisibleBuffer[ti]);
            gl.vertexAttribPointer(a.aDispose, this._vehicleVisibleBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._positionHighBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPositionHigh,
                this._positionHighBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._positionLowBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPositionLow,
                this._positionLowBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this._indicesBuffer[ti]);

            if (tagData.iCounts) {
                gl.drawElementsInstanced(
                    gl.TRIANGLES,
                    this._indicesBuffer[ti].numItems / tagData.iCounts,
                    gl.UNSIGNED_SHORT,
                    0,
                    tagData.iCounts
                );
            } else {
                gl.drawElements(
                    gl.TRIANGLES,
                    this._indicesBuffer[ti].numItems,
                    gl.UNSIGNED_SHORT,
                    0
                );
            }
        }
        gl.disable(gl.CULL_FACE);
    }

    drawPicking() {
        if (this._geoObjects.length && this.pickingEnabled) {
            this._pickingPASS();
        }
    }

    _pickingPASS() {
        const r = this._renderer,
            sh = r.handler.programs.geo_object_picking,
            p = sh._program,
            u = p.uniforms,
            a = p.attributes,
            gl = r.handler.gl,
            ec = this._entityCollection;

        sh.activate();

        gl.enable(gl.CULL_FACE);
        gl.uniform3fv(u.uScaleByDistance, ec.scaleByDistance);

        gl.uniform1f(u.pickingScale, ec.pickingScale);

        gl.uniform3fv(u.eyePositionHigh, r.activeCamera.eyeHigh);
        gl.uniform3fv(u.eyePositionLow, r.activeCamera.eyeLow);

        gl.uniformMatrix4fv(u.projectionMatrix, false, r.activeCamera.getProjectionMatrix());
        gl.uniformMatrix4fv(u.viewMatrix, false, r.activeCamera.getViewMatrix());

        for (const tag of this._instancedTags) {
            const tagData = tag[1],
                ti = tagData.index;

            gl.bindBuffer(gl.ARRAY_BUFFER, this._vertexBuffer[ti]);
            gl.vertexAttribPointer(
                a.aVertexPosition,
                this._vertexBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._directionBuffer[ti]);
            gl.vertexAttribPointer(
                a.aDirection,
                this._directionBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._sizeBuffer[ti]);
            gl.vertexAttribPointer(a.aScale, this._sizeBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, this._pitchRollBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPitchRoll,
                this._pitchRollBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._pickingColorBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPickingColor,
                this._pickingColorBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._positionHighBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPositionHigh,
                this._positionHighBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._positionLowBuffer[ti]);
            gl.vertexAttribPointer(
                a.aPositionLow,
                this._positionLowBuffer[ti].itemSize,
                gl.FLOAT,
                false,
                0,
                0
            );

            gl.bindBuffer(gl.ARRAY_BUFFER, this._vehicleVisibleBuffer[ti]);
            gl.vertexAttribPointer(a.aDispose, this._vehicleVisibleBuffer[ti].itemSize, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this._indicesBuffer[ti]);

            if (tagData.iCounts) {
                gl.drawElementsInstanced(
                    gl.TRIANGLES,
                    this._indicesBuffer[ti].numItems / tagData.iCounts,
                    gl.UNSIGNED_SHORT,
                    0,
                    tagData.iCounts
                );
            } else {
                gl.drawElements(
                    gl.TRIANGLES,
                    this._indicesBuffer[ti].numItems,
                    gl.UNSIGNED_SHORT,
                    0
                );
            }
        }
        gl.disable(gl.CULL_FACE);
    }

    _recalculateIndices(startIndex) {
        const allIndices = this._indicesArr,
            goArr = this._geoObjects,
            maxIndicesByTags = new Array(this._instancedTags.size).fill(0);

        for (let gi = 0; gi < goArr.length; gi++) {
            const go = goArr[gi],
                ti = this.getTagIndexByObjectIndex(go._handlerIndex),
                gIndices = go._indices;

            for (let ii = 0; ii < gIndices.length; ii++) {
                const gIndex = gIndices[ii];

                const i = go._indicesCount * go._tagIndex + ii;
                if (go._tagIndex > 0) {
                    allIndices[ti][i] = gIndex + maxIndicesByTags[ti];
                    if (allIndices[ti][i] > maxIndicesByTags[ti]) {
                        maxIndicesByTags[ti] = allIndices[ti][i] + 1;
                    }
                } else {
                    allIndices[ti][i] = gIndex;
                    if (gIndex > maxIndicesByTags[ti]) {
                        maxIndicesByTags[ti] = gIndex + 1;
                    }
                }
            }
        }
    }

    _addIndices(g) {
        let i = g._handlerIndex;
        const allIndices = this._indicesArr,
            gArr = this._geoObjects,
            iLen = g._indices.length,
            tagData = this._instancedTags.get(g.tag),
            maxIndex = tagData.maxIndex,
            ti = tagData.index;

        allIndices[ti] = concatArrays(allIndices[ti], g._indices);

        while (gArr[i]) {
            const g = gArr[i];

            if (g._tagIndex > 0) {
                setParametersToArray(allIndices[ti], g._tagIndex, iLen, iLen, ...g._indices.reduce((acc, cur) => {
                    acc.push(cur + ((maxIndex + 1) * g._tagIndex));
                    return acc;
                }, []));
            }
            i++;

        }

    }

    _removeIndices(geoObject) {
        const allIndices = this._indicesArr,
            gArr = this._geoObjects,
            iLen = geoObject._indices.length,
            tagData = this._instancedTags.get(geoObject.tag),
            maxIndex = tagData.maxIndex,
            ti = tagData.index,
            count = tagData.iCounts;

        let i = geoObject._handlerIndex;

        this._indicesArr[ti] = spliceArray(this._indicesArr[ti], geoObject._tagIndex * geoObject._indicesCount, geoObject._indicesCount);

        while (gArr[i]) {
            if (geoObject.tag === gArr[i].tag) {
                if (count !== 0) {
                    const startI = (gArr[i]._tagIndex - 1) * iLen;
                    let stopI = startI + geoObject._indicesCount;
                    while (stopI > startI) {
                        this._indicesArr[ti][stopI - 1] = allIndices[ti][stopI - 1] - maxIndex - 1;
                        stopI--;
                    }
                } else {
                    allIndices[ti] = geoObject._indices;
                }
            }
            i++;

        }

    }

    setDirectionArr(index, direction) {
        const itemSize = 3,
            ob = this.getObjectByIndex(index),
            ti = this.getTagIndexByObjectIndex(index);
        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._directionArr[ti], ob._tagIndex, length, itemSize, direction.x, direction.y, direction.z);
        this._changedBuffers[DIRECTION_BUFFER] = true;
    }

    setVisibility(index, visibility) {
        const ob = this.getObjectByIndex(index),
            ti = this.getTagIndexByObjectIndex(index);

        setParametersToArray(this._vehicleVisibleArr[ti], ob._tagIndex, 1, 1, visibility ? 1 : 0);

        this._changedBuffers[VISIBLE_BUFFER] = true;
    }

    setPositionArr(index, positionHigh, positionLow) {
        const itemSize = 3,
            ob = this.getObjectByIndex(index),
            ti = this.getTagIndexByObjectIndex(index);
        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._positionHighArr[ti], ob._tagIndex, length, itemSize, positionHigh.x, positionHigh.y, positionHigh.z);

        // Low
        setParametersToArray(this._positionLowArr[ti], ob._tagIndex, length, itemSize, positionLow.x, positionLow.y, positionLow.z);

        this._changedBuffers[POSITION_BUFFER] = true;
    }

    setRgbaArr(index, rgba) {
        const itemSize = 4,
            ob = this.getObjectByIndex(index),
            ti = this.getTagIndexByObjectIndex(index);
        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._rgbaArr[ti], ob._tagIndex, length, itemSize, rgba.x, rgba.y, rgba.z, rgba.w);

        this._changedBuffers[RGBA_BUFFER] = true;
    }

    getTagIndexByObjectIndex(index) {
        return this._instancedTags.get(this.getObjectByIndex(index).tag).index;
    }

    getTagDataByObjectIndex(index) {
        return this._instancedTags.get(this.getObjectByIndex(index).tag);
    }

    setPickingColorArr(index, color) {
        const itemSize = 3,
            ti = this.getTagIndexByObjectIndex(index),
            ob = this.getObjectByIndex(index),
            x = color.x / 255,
            y = color.y / 255,
            z = color.z / 255;

        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._pickingColorArr[ti], ob._tagIndex, length, itemSize, x, y, z);
        this._changedBuffers[PICKINGCOLOR_BUFFER] = true;
    }

    setPitchRollArr(index, pitch, roll) {
        const itemSize = 2,
            ti = this.getTagIndexByObjectIndex(index),
            ob = this.getObjectByIndex(index);
        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._pitchRollArr[ti], ob._tagIndex, length, itemSize, pitch, roll);
        this._changedBuffers[PITCH_ROLL_BUFFER] = true;
    }

    setScaleArr(index, scale) {
        const itemSize = 1,
            ti = this.getTagIndexByObjectIndex(index),
            ob = this.getObjectByIndex(index);
        let length = ob._verticesCount * itemSize;

        if (ob.instanced) {
            length = itemSize;
        }

        setParametersToArray(this._sizeArr[ti], ob._tagIndex, length, itemSize, scale);
        this._changedBuffers[SIZE_BUFFER] = true;
    }

    refresh() {
        let i = this._changedBuffers.length;
        while (i--) {
            this._changedBuffers[i] = true;
        }
    }

    _removeGeoObjects() {
        let i = this._geoObjects.length;
        while (i--) {
            const bi = this._geoObjects[i];
            bi._handlerIndex = -1;
            bi._handler = null;
        }
        this._geoObjects.length = 0;
        this._geoObjects = [];
    }

    clear() {
        this._sizeArr = null;
        this._pitchRollArr = null;
        this._vertexArr = null;
        this._positionHighArr = null;
        this._positionLowArr = null;
        this._directionArr = null;
        this._rgbaArr = null;
        this._normalsArr = null;
        this._indicesArr = null;
        this._pickingColorArr = null;
        this._vehicleVisibleArr = null;

        this._pitchRollArr = [new Float32Array()];
        this._sizeArr = [new Float32Array()];
        this._vertexArr = [new Float32Array()];
        this._positionHighArr = [new Float32Array()];
        this._positionLowArr = [new Float32Array()];
        this._rgbaArr = [new Float32Array()];
        this._directionArr = [new Float32Array()];
        this._normalsArr = [new Float32Array()];
        this._indicesArr = [new Uint16Array()];
        this._pickingColorArr = [new Float32Array()];
        this._vehicleVisibleArr = [new Int8Array()];

        this._removeGeoObjects();
        this._deleteBuffers();
        this.refresh();
    }

    _deleteBuffers() {
        if (this._renderer) {
            const gl = this._renderer.handler.gl;
            gl.deleteBuffer(this._sizeBuffer);
            gl.deleteBuffer(this._pitchRollBuffer);
            gl.deleteBuffer(this._vertexBuffer);
            gl.deleteBuffer(this._positionHighBuffer);
            gl.deleteBuffer(this._positionLowBuffer);
            gl.deleteBuffer(this._rgbaBuffer);
            gl.deleteBuffer(this._indicesBuffer);
            gl.deleteBuffer(this._normalsBuffer);
            gl.deleteBuffer(this._directionBuffer);
            gl.deleteBuffer(this._pickingColorBuffer);
        }

        this._pitchRollBuffer = null;
        this._sizeBuffer = null;
        this._vertexBuffer = null;
        this._positionHighBuffer = null;
        this._positionLowBuffer = null;
        this._rgbaBuffer = null;
        this._indicesBuffer = null;
        this._normalsBuffer = null;
        this._directionBuffer = null;
        this._pickingColorBuffer = null;
    }

    update() {
        if (this._renderer) {
            let i = this._changedBuffers.length;
            while (i--) {
                if (this._changedBuffers[i]) {
                    this._buffersUpdateCallbacks[i].call(this);
                    this._changedBuffers[i] = false;
                }
            }
        }
    }

    draw() {
        if (this._geoObjects.length) {
            this.update();
            this._displayPASS();
        }
    }

    _reindexGeoObjects(startIndex, tag) {
        const b = this._geoObjects;

        for (let i = startIndex; i < b.length; i++) {
            const go = b[i];

            b[i]._handlerIndex = i;
            if (tag === go.tag) {
                --b[i]._tagIndex;
            }
        }
    }

    add(geoObject) {
        if (geoObject._handlerIndex === -1) {
            geoObject._handler = this;
            geoObject._handlerIndex = this._geoObjects.length;
            this._geoObjects.push(geoObject);
            this._addGeoObjectToArray(geoObject);
            this.refresh();
        }
    }

    remove(geoObject) {
        if (geoObject._handler && this.__staticId == geoObject._handler.__staticId) {
            this._removeGeoObject(geoObject);
        }
    }

    _removeGeoObject(geoObject) {
        const gi = geoObject._handlerIndex,
            tag = geoObject.tag,
            ti = this.getTagIndexByObjectIndex(gi),
            prevState = this._instancedTags.get(tag),
            iCount = prevState.iCounts - 1;

        this._instancedTags.set(tag, {
            ...prevState,
            iCounts: iCount
        });

        this._geoObjects.splice(gi, 1);

        let i = geoObject._tagIndex * 4;
        this._rgbaArr[ti] = spliceArray(this._rgbaArr[ti], i, 4);

        i = geoObject._tagIndex * 3;
        if (prevState.iCounts <= 1) {
            this._vertexArr[ti] = spliceArray(this._vertexArr[ti], 0, geoObject._verticesCount * 3);
            this._normalsArr[ti] = spliceArray(
                this._normalsArr[ti],
                0,
                geoObject._verticesCount * 3
            );
        }
        this._positionHighArr[ti] = spliceArray(this._positionHighArr[ti], i, 3);
        this._positionLowArr[ti] = spliceArray(this._positionLowArr[ti], i, 3);
        this._directionArr[ti] = spliceArray(this._directionArr[ti], i, 3);
        this._pickingColorArr[ti] = spliceArray(this._pickingColorArr[ti], i, 3);

        i = geoObject._tagIndex * 2;
        this._pitchRollArr[ti] = spliceArray(this._pitchRollArr[ti], i, 2);
        i = geoObject._tagIndex;
        this._sizeArr[ti] = spliceArray(this._sizeArr[ti], i, 1);
        this._vehicleVisibleArr[ti] = spliceArray(this._vehicleVisibleArr[ti], i, 1);

        this._removeIndices(geoObject);

        this._reindexGeoObjects(gi, tag);

        this.refresh();

        geoObject._handlerIndex = -1;
        geoObject._handler = null;
    }
}

export { GeoObjectHandler };
