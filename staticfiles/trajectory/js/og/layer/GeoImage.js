/**
 * @module og/layer/GeoImage
 */

"use strict";

import { BaseGeoImage } from "./BaseGeoImage.js";

/**
 * Used to load and display a single image over specific corner coordinates on the globe, implements og.layer.BaseGeoImage interface.
 * @class
 * @extends {BaseGeoImage}
 */
class GeoImage extends BaseGeoImage {
    constructor(name, options) {
        super(name, options);

        /**
         * Image object.
         * @private
         * @type {Image}
         */
        this._image = options.image || null;

        /**
         * Image source url path.
         * @private
         * @type {String}
         */
        this._src = options.src || null;
    }

    get instanceName() {
        return "GeoImage";
    }

    /**
     * Sets image source url path.
     * @public
     * @param {String} srs - Image url path.
     */
    setSrc(src) {
        this._planet && this._planet._geoImageCreator.remove(this);
        this._src = src;
        this._sourceReady = false;
    }

    /**
     * Sets image object.
     * @public
     * @param {Image} image - Image object.
     */
    setImage(image) {
        this._planet && this._planet._geoImageCreator.remove(this);
        this._image = image;
        this._src = image.src;
        this._sourceReady = false;
    }

    /**
     * Creates source gl texture.
     * @virtual
     * @protected
     */
    _createSourceTexture() {
        if (!this._sourceCreated) {
            this._sourceTexture = this._planet.renderer.handler.createTexture_n(this._image);
            this._sourceCreated = true;
        }
    }

    /**
     * @private
     * @param {Image} img
     */
    _onLoad(img) {
        this._frameWidth = img.width;
        this._frameHeight = img.height;
        this._sourceReady = true;
        this._planet._geoImageCreator.add(this);
    }

    /**
     * Loads planet segment material. In this case - GeoImage source image.
     * @virtual
     * @public
     * @param {Material} material - GeoImage planet material.
     */
    loadMaterial(material) {
        material.isLoading = true;
        this._creationProceeding = true;
        if (!this._sourceReady && this._src) {
            if (this._image) {
                if (this._image.complete) {
                    this._onLoad(this._image);
                } else if (this._image.src) {
                    let that = this;
                    this._image.addEventListener("load", function (e) {
                        that._onLoad(this);
                    });
                }
            } else {
                let that = this;
                this._image = new Image();
                this._image.addEventListener("load", function (e) {
                    that._onLoad(this);
                });
                this._image.src = this._src;
            }
        } else {
            this._planet._geoImageCreator.add(this);
        }
    }

    /**
     * @virtual
     * @param {Material} material - GeoImage material.
     */
    abortMaterialLoading(material) {
        this._image && (this._image.src = "");
        this._creationProceeding = false;
        material.isLoading = false;
        material.isReady = false;
    }

    _renderingProjType1() {
        var p = this._planet,
            h = p.renderer.handler,
            gl = h.gl,
            creator = p._geoImageCreator;

        this._refreshFrame && this._createFrame();
        this._createSourceTexture();

        var f = creator._framebuffer;
        f.setSize(this._frameWidth, this._frameHeight);
        f.activate();

        h.programs.geoImageTransform.activate();
        var sh = h.programs.geoImageTransform._program;
        var sha = sh.attributes,
            shu = sh.uniforms;

        gl.disable(gl.CULL_FACE);

        f.bindOutputTexture(this._materialTexture);
        gl.clearColor(0.0, 0.0, 0.0, 0.0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.bindBuffer(gl.ARRAY_BUFFER, creator._texCoordsBuffer);

        gl.vertexAttribPointer(sha.texCoords, 2, gl.UNSIGNED_SHORT, true, 0, 0);

        gl.bindBuffer(gl.ARRAY_BUFFER, this._gridBuffer);
        gl.vertexAttribPointer(sha.corners, this._gridBuffer.itemSize, gl.FLOAT, false, 0, 0);
        gl.uniform4fv(shu.extentParams, this._extentMercParams);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this._sourceTexture);
        gl.uniform1i(shu.sourceTexture, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, creator._indexBuffer);
        gl.drawElements(gl.TRIANGLE_STRIP, creator._indexBuffer.numItems, gl.UNSIGNED_INT, 0);
        f.deactivate();

        gl.enable(gl.CULL_FACE);

        this._ready = true;

        this._creationProceeding = false;
    }

    _renderingProjType0() {
        var p = this._planet,
            h = p.renderer.handler,
            gl = h.gl,
            creator = p._geoImageCreator;

        this._refreshFrame && this._createFrame();
        this._createSourceTexture();

        var f = creator._framebuffer;
        f.setSize(this._frameWidth, this._frameHeight);
        f.activate();

        h.programs.geoImageTransform.activate();
        var sh = h.programs.geoImageTransform._program;
        var sha = sh.attributes,
            shu = sh.uniforms;

        gl.disable(gl.CULL_FACE);

        f.bindOutputTexture(this._materialTexture);
        gl.clearColor(0.0, 0.0, 0.0, 0.0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.bindBuffer(gl.ARRAY_BUFFER, creator._texCoordsBuffer);

        gl.vertexAttribPointer(sha.texCoords, 2, gl.UNSIGNED_SHORT, true, 0, 0);

        gl.bindBuffer(gl.ARRAY_BUFFER, this._gridBuffer);
        gl.vertexAttribPointer(sha.corners, this._gridBuffer.itemSize, gl.FLOAT, false, 0, 0);
        gl.uniform4fv(shu.extentParams, this._extentWgs84Params);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this._sourceTexture);
        gl.uniform1i(shu.sourceTexture, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, creator._indexBuffer);
        gl.drawElements(gl.TRIANGLE_STRIP, creator._indexBuffer.numItems, gl.UNSIGNED_INT, 0);
        f.deactivate();

        gl.enable(gl.CULL_FACE);

        this._ready = true;

        this._creationProceeding = false;
    }
}

export { GeoImage };