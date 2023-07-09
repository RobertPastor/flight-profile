#How to rebuild the final og after applying modifications


## install node.js if needed

## install git / git Bash

in gitBash launch 
$ git clone https://github.com/openglobus/openglobus.git


## ============= npm install ===============

go to the repo and launch PowerShell

PS D:\Node.js\openglobus.0.13.7> npm install

## =================== npm run build ==============================

PS D:\Node.js\openglobus.0.13.7> npm run build

> @openglobus/og@0.13.7 build D:\Node.js\openglobus.0.13.7
> rollup -c


src/og/index.js → dist/@openglobus/og.umd.js...
(!) Circular dependencies
src\og\Extent.js -> src\og\mercator.js -> src\og\Extent.js
src\og\mercator.js -> src\og\LonLat.js -> src\og\mercator.js
src\og\math\Vec3.js -> src\og\math\Vec4.js -> src\og\math\Vec3.js
...and 8 more
created dist/@openglobus/og.umd.js in 6.5s

src/og/index.js → dist/@openglobus/og.esm.js...
(!) Circular dependencies
src\og\Extent.js -> src\og\mercator.js -> src\og\Extent.js
src\og\mercator.js -> src\og\LonLat.js -> src\og\mercator.js
src\og\math\Vec3.js -> src\og\math\Vec4.js -> src\og\math\Vec3.js
...and 8 more
created dist/@openglobus/og.esm.js in 5.6s

css/og.css → dist/@openglobus/og.css...
Browserslist: caniuse-lite is outdated. Please run:
  npx browserslist@latest --update-db
  Why you should do it regularly: https://github.com/browserslist/browserslist#browsers-data-updating
(!) The emitted file "og.css" overwrites a previously emitted file of the same name.
created dist/@openglobus/og.css in 686ms
PS D:\Node.js\openglobus.0.13.7>

#================== build ===============================

PS D:\Node.js\openglobus> npm run build

> @openglobus/og@0.12.4 build D:\Node.js\openglobus
> rollup -c


src/og/index.js → dist/@openglobus/og.umd.js...
(!) Circular dependencies
src\og\Extent.js -> src\og\mercator.js -> src\og\Extent.js
src\og\mercator.js -> src\og\LonLat.js -> src\og\mercator.js
src\og\math\Vec3.js -> src\og\math\Vec4.js -> src\og\math\Vec3.js
...and 8 more
created dist/@openglobus/og.umd.js in 6.3s

src/og/index.js → dist/@openglobus/og.esm.js...
(!) Circular dependencies
src\og\Extent.js -> src\og\mercator.js -> src\og\Extent.js
src\og\mercator.js -> src\og\LonLat.js -> src\og\mercator.js
src\og\math\Vec3.js -> src\og\math\Vec4.js -> src\og\math\Vec3.js
...and 8 more
created dist/@openglobus/og.esm.js in 5.3s

css/og.css → dist/@openglobus/og.css...
Browserslist: caniuse-lite is outdated. Please run:
  npx browserslist@latest --update-db
  Why you should do it regularly: https://github.com/browserslist/browserslist#browsers-data-updating
(!) The emitted file "og.css" overwrites a previously emitted file of the same name.
created dist/@openglobus/og.css in 665ms
PS D:\Node.js\openglobus>



#=========== avoid minifying ======================

to avoid compressing minifying 

in file rollup.config.js suppress terser in the 1st plugin before the json() plugin

export default [
    {
        input: `src/og/index${LIB_SUFFIX}.js`,
        output: [
            {
                file: `${OUTPUT_NAME}umd.js`,
                format: "umd",
                name: "og",
                sourcemap: true
            }
        ],
        plugins: [json() ]
        
        
in order to avoid minifying og.css , change minimize: true with minimize: false in og.css section

minimize: false

##================== build again ===============================

npm run build

#=================== copy files to the flight profile folder ==============

copy from D:\Node.js\openglobus\dist\@openglobus
1) og.umd.js
2) og.umd.js.map

to the project static js folder : /flight-profile/trajectory/static/js/og


## ====================== apply patches

## add function to KML layer

layerKML.addKmlFromXml(  xmlDoc ,  null ,  null );

/**
	* Robert - 18th July 2022
	* @public
	* @param {string} [color]
    * @param {Billboard} [billboard]
    * @returns {Promise<{entities: Entity[], extent: Extent}>}
	*/
	async addKmlFromXml( kmlAsXml , color = null, billboard = null ) {
		const coordinates = this._extractCoordonatesFromKml(kmlAsXml);
        const { entities, extent } = this._convertCoordonatesIntoEntities(
            [coordinates],
            color || this._color,
            billboard || this._billboard
        );
        this._extent = this._expandExtents(this._extent, extent);
        entities.forEach(this.add.bind(this));
        return { entities, extent };
		
	}


## in GlobusTerrain _createHeights

/**
     * Converts loaded data to segment elevation data type(colum major elevation data array in meters)
     * @public
     * @virtual
     * @param {*} data - Loaded elevation data.
     * @returns {Array.<number>} -
     */
    _createHeights(data) {
		// Robert - 11-dec-2022 - error Float32Array size should be multiple of 4
		var len = data.byteLength;
		len = len - (len % 4);
        return new Float32Array(data.slice(0,len));
    }
    
    
## in Class Loader

 _exec() {

        if (this._queue.length > 0 && this._loading < this.MAX_REQUESTS) {

            let q = this._queue.pop(),
                p = q.params;

            if (!p.filter || p.filter(p)) {

                this._loading++;

				// 12-Dec-2022 - Robert - path to avoid warning messages
				try {
					return fetch(p.src, p.options || {})
						.then(response => {
							if (!response.ok) {
								throw Error(`Unable to load '${p.src}'`);
							}
							return this._promises[p.type || "blob"](response);
						})
						.then(data => {
							this._loading--;
							this._handleResponse(q, { status: "ready", data: data });
						})
						.catch(err => {
							this._loading--;
							this._handleResponse(q, { status: "error", msg: err.toString() });
						});
				} catch ( err ) {
					this._loading--;
					this._handleResponse(q, { status: "error", msg: err.toString() });
				}

            } else {
                this._handleResponse(q, { status: "abort" });
            }
        } else if (this._loading === 0) {
            this.events.dispatch(this.events.loadend);
        }
    }

    
##  see also modifications in og.css

 