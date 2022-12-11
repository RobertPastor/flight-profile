#How to rebuild the final og after applying modifications


go to the repo and launch PowerShell

PS D:\Node.js\openglobus.0.13.7> npm install

#=================================================

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

#=================================================

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

#=================================
copy from D:\Node.js\openglobus\dist\@openglobus
1) og.umd.js
2) og.umd.js.map

to the project static js folder : /flight-profile/trajectory/static/js/og

#=========== avoid compressing ======================
to avoid compressing minifying 

in file rollup.config.js suppress terser in the 1st plugin befiore the json() plugin

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
        plugins: [json()]

# apply patches

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
     * Converts loaded data to segment elevation data type(columr major elevation data array in meters)
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
