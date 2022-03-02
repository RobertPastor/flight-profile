/**
 * @module og/layer/Layer
 */

"use strict";

import * as utils from "../utils/shared.js";
import * as mercator from "../mercator.js";
import { Events } from "../Events.js";
import { Extent } from "../Extent.js";
import { LonLat } from "../LonLat.js";
import { Material } from "./Material.js";
import { Vec3 } from "../math/Vec3.js";

export const FADING_FACTOR = 0.29;

/**
 * @classdesc
 * Base class; normally only used for creating subclasses and not instantiated in apps.
 * A visual representation of raster or vector map data well known as a layer.
 * @class
 * @param {String} [name="noname"] - Layer name.
 * @param {Object} [options] - Layer options:
 * @param {number} [options.opacity=1.0] - Layer opacity.
 * @param {number} [options.minZoom=0] - Minimal visibility zoom level.
 * @param {number} [options.maxZoom=0] - Maximal visibility zoom level.
 * @param {string} [options.attribution] - Layer attribution that displayed in the attribution area on the screen.
 * @param {boolean} [options.isBaseLayer=false] - This is a base layer.
 * @param {boolean} [options.visibility=true] - Layer visibility.
 * @param {boolean} [options.isSRGB=false] - Layer image webgl nternal format.
 * @param {Extent} [options.extent=[[-180.0, -90.0], [180.0, 90.0]]] - Visible extent.
 * @param {string} [options.textureFilter="anisotropic"] - Image texture filter. Available values: "nearest", "linear", "mipmap" and "anisotropic".
 *
 * @fires og.Layer#visibilitychange
 * @fires og.Layer#add
 * @fires og.Layer#remove
 * @fires og.layer.Vector#mousemove
 * @fires og.layer.Vector#mouseenter
 * @fires og.layer.Vector#mouseleave
 * @fires og.layer.Vector#lclick
 * @fires og.layer.Vector#rclick
 * @fires og.layer.Vector#mclick
 * @fires og.layer.Vector#ldblclick
 * @fires og.layer.Vector#rdblclick
 * @fires og.layer.Vector#mdblclick
 * @fires og.layer.Vector#lup
 * @fires og.layer.Vector#rup
 * @fires og.layer.Vector#mup
 * @fires og.layer.Vector#ldown
 * @fires og.layer.Vector#rdown
 * @fires og.layer.Vector#mdown
 * @fires og.layer.Vector#lhold
 * @fires og.layer.Vector#rhold
 * @fires og.layer.Vector#mhold
 * @fires og.layer.Vector#mousewheel
 * @fires og.layer.Vector#touchmove
 * @fires og.layer.Vector#touchstart
 * @fires og.layer.Vector#touchend
 * @fires og.layer.Vector#doubletouch
 */
class Layer {
    constructor(name, options = {}) {
        /**
         * Layer user name.
         * @public
         * @type {string}
         */
        this.name = name || "noname";

        this._labelMaxLetters = options.labelMaxLetters;

        this.displayInLayerSwitcher =
            options.displayInLayerSwitcher !== undefined ? options.displayInLayerSwitcher : true;

        this._hasImageryTiles = true;

        /**
         * Layer global opacity.
         * @public
         * @type {number}
         */
        this._opacity = options.opacity || 1.0;

        /**
         * Minimal zoom level when layer is visibile.
         * @public
         * @type {number}
         */
        this.minZoom = options.minZoom || 0;

        /**
         * Maximal zoom level when layer is visibile.
         * @public
         * @type {number}
         */
        this.maxZoom = options.maxZoom || 50;

        /**
         * Planet node.
         * @protected
         * @type {Planet}
         */
        this._planet = null;

        /**
         * Unic identifier.
         * @protected
         * @type {number}
         */
        this._id = Layer.__layersCounter++;

        /**
         * Layer attribution.
         * @protected
         * @type {string}
         */
        this._attribution = options.attribution || "";

        /**
         * Layer z-index.
         * @protected
         * @type {number}
         */
        this._zIndex = options.zIndex || 0;

        /**
         * Base layer type flag.
         * @protected
         * @type {boolean}
         */
        this._isBaseLayer = options.isBaseLayer || false;

        this._defaultTextures = options.defaultTextures || [null, null];

        /**
         * Layer visibility.
         * @protected
         * @type {boolean}
         */
        this._visibility = options.visibility !== undefined ? options.visibility : true;

        this._fading = options.fading || false;

        this._fadingFactor = FADING_FACTOR;

        if (this._fading) {
            this._fadingOpacity = this._visibility ? this._opacity : 0.0;
        } else {
            this._fadingOpacity = this._opacity;
        }

        /**
         * Height over the ground.
         * @protected
         * @type {number}
         */
        this._height = options.height || 0;

        /**
         * Visible degrees extent.
         * @protected
         * @type {Extent}
         */
        this._extent = null;

        this.createTexture = null;

        this._textureFilter = options.textureFilter ? options.textureFilter.trim().toUpperCase() : "MIPMAP";

        this._isSRGB = options.isSRGB != undefined ? options.isSRGB : false;

        this._internalFormat = null;

        /**
         * Visible mercator extent.
         * @protected
         * @type {Extent}
         */
        this._extentMerc = null;

        // Setting the extent up
        this.setExtent(
            utils.createExtent(
                options.extent,
                new Extent(new LonLat(-180, -90), new LonLat(180, 90))
            )
        );

        /**
         * Layer picking color. Assign when added to the planet.
         * @protected
         * @type {Vec3}
         */
        this._pickingColor = new Vec3();

        this._pickingEnabled = options.pickingEnabled !== undefined ? options.pickingEnabled : true;

        this._isPreloadDone = false;

        this._preLoadZoomLevels = options.preLoadZoomLevels || [0, 1];

        /**
         * Events handler.
         * @public
         * @type {Events}
         */
        this.events = new Events(EVENT_NAMES, this);
    }

    static getTMS(x, y, z) {
        return {
            x: x,
            y: (1 << z) - y - 1,
            z: z
        };
    }

    static getTileIndex(...arr) {
        return arr.join("_");
    }

    static get __layersCounter() {
        if (!this.__lcounter && this.__lcounter !== 0) {
            this.__lcounter = 0;
        }
        return this.__lcounter;
    }

    static set __layersCounter(n) {
        this.__lcounter = n;
    }

    static get __requestsCounter() {
        return this.__reqcounter;
    }

    static set __requestsCounter(v) {
        this.__reqcounter = v;
    }

    /**
     * Maximum loading queries at one time.
     * @const
     * @type {number}
     */
    static get MAX_REQUESTS() {
        return 7;
    }

    get instanceName() {
        return "Layer";
    }

    get rendererEvents() {
        return this.events;
    }

    set opacity(opacity) {
        if (this._fading) {
            if (opacity > this._opacity) {
                this._fadingFactor = (opacity - this._opacity) / 2.8;
            } else if (opacity < this._opacity) {
                this._fadingFactor = (opacity - this._opacity) / 2.8;
            }
        } else {
            this._fadingOpacity = opacity;
        }
        this._opacity = opacity;
    }

    get opacity() {
        return this._opacity;
    }

    set pickingEnabled(picking) {
        this._pickingEnabled = picking ? 1.0 : 0.0;
    }

    get pickingEnabled() {
        return !!this._pickingEnabled;
    }

    /**
     * Returns true if a layer has imagery tiles.
     * @public
     * @virtual
     * @returns {boolean} - Imagery tiles flag.
     */
    hasImageryTiles() {
        return this._hasImageryTiles;
    }

    /**
     * Gets layer identifier.
     * @public
     * @returns {string} - Layer object id.
     */
    getID() {
        return this._id;
    }

    /**
     * Compares layers instances.
     * @public
     * @param {Layer} layer - Layer instance to compare.
     * @returns {boolean} - Returns true if the layers is the same instance of the input.
     */
    isEqual(layer) {
        return layer._id === this._id;
    }

    /**
     * Assign the planet.
     * @protected
     * @virtual
     * @param {Planet} planet - Planet render node.
     */
    _assignPlanet(planet) {
        // TODO: webgl1
        if (this._isSRGB) {
            this._internalFormat = planet.renderer.handler.gl.SRGB8_ALPHA8;
        } else {
            this._internalFormat = planet.renderer.handler.gl.RGBA8;
        }

        this.createTexture = planet.renderer.handler.createTexture[this._textureFilter];

        planet.layers.push(this);
        this._planet = planet;
        this.events.on("visibilitychange", planet._onLayerVisibilityChanged, planet);
        if (this._isBaseLayer && this._visibility) {
            planet.setBaseLayer(this);
        }

        if (this._visibility) {
            this._preLoad();
        }

        planet.events.dispatch(planet.events.layeradd, this);
        this.events.dispatch(this.events.add, planet);
        planet.updateVisibleLayers();
        this._bindPicking();
    }

    /**
     * Assign picking color to the layer.
     * @protected
     * @virtual
     */
    _bindPicking() {
        this._planet && this._planet.renderer.assignPickingColor(this);
    }

    /**
     * Adds layer to the planet.
     * @public
     * @param {Planet} planet - Adds layer to the planet.
     */
    addTo(planet) {
        if (!this._planet) {
            this._assignPlanet(planet);
        }
        return this;
    }

    /**
     * Removes from planet.
     * @public
     * @returns {Layer} -This layer.
     */
    remove() {
        var p = this._planet;
        if (p) {
            for (var i = 0; i < p.layers.length; i++) {
                if (this.isEqual(p.layers[i])) {
                    p.renderer.clearPickingColor(this);
                    p.layers.splice(i, 1);
                    p.updateVisibleLayers();
                    this.clear();
                    p.events.dispatch(p.events.layerremove, this);
                    this.events.dispatch(this.events.remove, p);
                    this._planet = null;
                    return this;
                }
            }
        }
        return this;
    }

    /**
     * Clears layer material.
     * @virtual
     */
    clear() {
        if (this._planet) {
            this._planet._clearLayerMaterial(this);
            this._internalFormat = null;
            this.createTexture = null;
        }
    }

    /**
     * Returns planet instance.
     * @virtual
     */
    get planet() {
        return this._planet;
    }

    /**
     * Sets layer attribution text.
     * @public
     * @param {string} html - HTML code that represents layer attribution, it could be just a text.
     */
    setAttribution(html) {
        this._attribution = html;
        this._planet && this._planet.updateAttributionsList();
    }

    /**
     * Sets height over the ground.
     * @public
     * @param {number} height - Layer height.
     */
    setHeight(height) {
        this._height = height;
        this._planet && this._planet.updateVisibleLayers();
    }

    /**
     * Gets layer height.
     * @public
     * @returns {number} -
     */
    getHeight() {
        return this._height;
    }

    /**
     * Sets z-index.
     * @public
     * @param {number} zIndex - Layer z-index.
     */
    setZIndex(zIndex) {
        this._zIndex = zIndex;
        this._planet && this._planet.updateVisibleLayers();
    }

    /**
     * Gets z-index.
     * @public
     * @returns {number} -
     */
    getZIndex() {
        return this._zIndex;
    }

    /**
     * Set zIndex to the maximal value depend on other layers on the planet.
     * @public
     */
    bringToFront() {
        if (this._planet) {
            var vl = this._planet.visibleTileLayers;
            var l = vl[vl.length - 1];
            if (!l.isEqual(this)) {
                this.setZIndex(l.getZIndex() + 1);
            }
        }
    }

    /**
     * Returns true if the layer is a base.
     * @public
     * @returns {boolean} - Base layer flag.
     */
    isBaseLayer() {
        return this._isBaseLayer;
    }

    /**
     * Sets base layer type true.
     * @public
     * @param {boolean} flag - Base layer flag.
     */
    setBaseLayer(flag) {
        this._isBaseLayer = flag;
        if (this._planet) {
            if (!flag && this.isEqual(this._planet.baseLayer)) {
                this._planet.baseLayer = null;
            }
            this._planet.updateVisibleLayers();
        }
    }

    /**
     * Sets layer visibility.
     * @public
     * @virtual
     * @param {boolean} visibility - Layer visibility.
     */
    setVisibility(visibility) {
        if (visibility !== this._visibility) {
            this._visibility = visibility;
            if (this._planet) {
                if (this._isBaseLayer && visibility) {
                    this._planet.setBaseLayer(this);
                }
                this._planet.updateVisibleLayers();
                if (visibility && !this._isPreloadDone && !this.isVector) {
                    this._isPreloadDone = true;
                    this._preLoad();
                }
            }
            this.events.dispatch(this.events.visibilitychange, this);
        }
    }

    _forceMaterialApply(segment) {
        let pm = segment.materials,
            m = pm[this._id];

        if (!m) {
            m = pm[this._id] = this.createMaterial(segment);
        }

        if (!m.isReady) {
            this._planet._renderCompleted = false;
        }

        this.applyMaterial(m);
    }

    _preLoadRecursive(node, maxZoom) {
        if (node.segment.tileZoom > maxZoom) {
            return;
        }
        if (this._preLoadZoomLevels.includes(node.segment.tileZoom)) {
            this._forceMaterialApply(node.segment);
        }

        for (let i = 0, len = node.nodes.length; i < len; i++) {
            if (node.nodes[i]) {
                this._preLoadRecursive(node.nodes[i], maxZoom);
            }
        }
    }

    _preLoad() {
        if (this._planet && this._preLoadZoomLevels.length) {

            let p = this._planet,
                maxZoom = Math.max(...this._preLoadZoomLevels);

            this._preLoadRecursive(p._quadTreeSouth, maxZoom);
            this._preLoadRecursive(p._quadTreeNorth, maxZoom);
            this._preLoadRecursive(p._quadTree, maxZoom);
        }
    }

    /**
     * Gets layer visibility.
     * @public
     * @returns {boolean} - Layer visibility.
     */
    getVisibility() {
        return this._visibility;
    }

    /**
     * Sets visible geographical extent.
     * @public
     * @param {Extent} extent - Layer visible geographical extent.
     */
    setExtent(extent) {
        var sw = extent.southWest.clone(),
            ne = extent.northEast.clone();
        if (sw.lat < mercator.MIN_LAT) {
            sw.lat = mercator.MIN_LAT;
        }
        if (ne.lat > mercator.MAX_LAT) {
            ne.lat = mercator.MAX_LAT;
        }
        this._extent = extent.clone();
        this._extentMerc = new Extent(sw.forwardMercator(), ne.forwardMercator());
        this._correctFullExtent();
    }

    /**
     * Gets layer extent.
     * @public
     * @return {Extent} - Layer geodetic extent.
     */
    getExtent() {
        return this._extent;
    }

    /**
     * Special correction of the whole globe extent.
     * @protected
     */
    _correctFullExtent() {
        // var e = this._extent,
        //    em = this._extentMerc;
        // var ENLARGE_MERCATOR_LON = og.mercator.POLE + 50000;
        // var ENLARGE_MERCATOR_LAT = og.mercator.POLE + 50000;
        // if (e.northEast.lat === 90.0) {
        //    em.northEast.lat = ENLARGE_MERCATOR_LAT;
        // }
        // if (e.northEast.lon === 180.0) {
        //    em.northEast.lon = ENLARGE_MERCATOR_LON;
        // }
        // if (e.southWest.lat === -90.0) {
        //    em.southWest.lat = -ENLARGE_MERCATOR_LAT;
        // }
        // if (e.southWest.lon === -180.0) {
        //    em.southWest.lon = -ENLARGE_MERCATOR_LON;
        // }
    }

    _refreshFadingOpacity() {
        var p = this._planet;
        if (
            this._visibility &&
            p._viewExtent &&
            p._viewExtent.overlaps(this._extent) &&
            p.maxCurrZoom >= this.minZoom &&
            p.minCurrZoom <= this.maxZoom
        ) {
            this._fadingOpacity += this._fadingFactor;

            if (
                (this._fadingFactor > 0.0 && this._fadingOpacity > this._opacity) ||
                (this._fadingFactor < 0.0 && this._fadingOpacity < this._opacity)
            ) {
                this._fadingOpacity = this._opacity;
            }
            return false;
        } else {
            this._fadingOpacity -= FADING_FACTOR;

            if (this._fadingOpacity < 0.0) {
                this._fadingOpacity = 0.0;
                return !this._visibility;
            }
        }
    }

    createMaterial(segment) {
        return new Material(segment, this);
    }
}

const EVENT_NAMES = [
    /**
     * Triggered when layer visibilty chanched.
     * @event og.Layer#visibilitychange
     */
    "visibilitychange",

    /**
     * Triggered when layer has added to the planet.
     * @event og.Layer#add
     */
    "add",

    /**
     * Triggered when layer has removed from the planet.
     * @event og.Layer#remove
     */
    "remove",

    /**
     * Triggered when mouse moves over the layer.
     * @event og.Layer#mousemove
     */
    "mousemove",

    /**
     * Triggered when mouse has entered over the layer.
     * @event og.Layer#mouseenter
     */
    "mouseenter",

    /**
     * Triggered when mouse leaves the layer.
     * @event og.Layer#mouseenter
     */
    "mouseleave",

    /**
     * Mouse left button clicked.
     * @event og.Layer#lclick
     */
    "lclick",

    /**
     * Mouse right button clicked.
     * @event og.Layer#rclick
     */
    "rclick",

    /**
     * Mouse right button clicked.
     * @event og.Layer#mclick
     */
    "mclick",

    /**
     * Mouse left button double click.
     * @event og.Layer#ldblclick
     */
    "ldblclick",

    /**
     * Mouse right button double click.
     * @event og.Layer#rdblclick
     */
    "rdblclick",

    /**
     * Mouse middle button double click.
     * @event og.Layer#mdblclick
     */
    "mdblclick",

    /**
     * Mouse left button up(stop pressing).
     * @event og.Layer#lup
     */
    "lup",

    /**
     * Mouse right button up(stop pressing).
     * @event og.Layer#rup
     */
    "rup",

    /**
     * Mouse middle button up(stop pressing).
     * @event og.Layer#mup
     */
    "mup",

    /**
     * Mouse left button is just pressed down(start pressing).
     * @event og.Layer#ldown
     */
    "ldown",

    /**
     * Mouse right button is just pressed down(start pressing).
     * @event og.Layer#rdown
     */
    "rdown",

    /**
     * Mouse middle button is just pressed down(start pressing).
     * @event og.Layer#mdown
     */
    "mdown",

    /**
     * Mouse left button is pressing.
     * @event og.Layer#lhold
     */
    "lhold",

    /**
     * Mouse right button is pressing.
     * @event og.Layer#rhold
     */
    "rhold",

    /**
     * Mouse middle button is pressing.
     * @event og.Layer#mhold
     */
    "mhold",

    /**
     * Mouse wheel is rotated.
     * @event og.Layer#mousewheel
     */
    "mousewheel",

    /**
     * Triggered when touching moves over the layer.
     * @event og.Layer#touchmove
     */
    "touchmove",

    /**
     * Triggered when layer begins to touch.
     * @event og.Layer#touchstart
     */
    "touchstart",

    /**
     * Triggered when layer has finished touching.
     * @event og.Layer#touchend
     */
    "touchend",

    /**
     * Triggered layer has double touched.
     * @event og.Layer#doubletouch
     */
    "doubletouch",

    /**
     * Triggered when touching leaves layer borders.
     * @event og.Layer#touchleave
     */
    "touchleave",

    /**
     * Triggered when touch enters over the layer.
     * @event og.Layer#touchenter
     */
    "touchenter"
];

export { Layer };
