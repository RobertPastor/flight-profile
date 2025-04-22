#How to rebuild the final og after applying modifications


## install node.js if needed

## install git / git Bash

## ====== move to the node.js folder -> 

$ pwd
/c/Users/rober

rober@RobertPastor MINGW64 ~
$ cd node.js/

rober@RobertPastor MINGW64 ~/node.js
$ ls
openglobus.0.17.0/

rober@RobertPastor MINGW64 ~/node.js
$

## ===== in the node.js target folder -> git clone 

in gitBash launch 
$ git clone https://github.com/openglobus/openglobus.git

rober@RobertPastor MINGW64 ~/node.js
$ git clone https://github.com/openglobus/openglobus.git
Cloning into 'openglobus'...
remote: Enumerating objects: 43336, done.
remote: Counting objects: 100% (193/193), done.
remote: Compressing objects: 100% (163/163), done.
remote: Total 43336 (delta 54), reused 64 (delta 28), pack-reused 43143 (from 2)
Receiving objects: 100% (43336/43336), 162.31 MiB | 20.38 MiB/s, done.
Resolving deltas: 100% (29547/29547), done.

rober@RobertPastor MINGW64 ~/node.js

## ===== the openglobus version is contained in the package.json filet

$ cat package.json
{
  "name" : "@openglobus/og",
  "version" : "0.25.5",


## ============= npm install ===============

go to the repo and launch PowerShelll

PS D:\Node.js\openglobus.0.13.7> npm install

this command should create a node_modules folder


## ============== if needed upgrade the node.js version

l$ node -v
v22.14.0

rober@RobertPastor MINGW64 ~/node.js/openglobus (master)


## =================== npm run build ==============================

PS D:\Node.js\openglobus.0.13.7> npm run buildd

$ npm run build

> @openglobus/og@0.25.5 build
> vite build --mode production && npm run dts

vite v6.2.6 building for production...
transforming...
✓ 276 modules transformed.
rendering chunks...
computing gzip size...
[vite-plugin-static-copy] Copied 1 items.
lib/og.css       19.84 kB │ gzip:   4.97 kB
lib/og.es.js  1,093.96 kB │ gzip: 231.52 kB
✓ built in 4.60s
✔ ./lib/og.es.js minified with terser

> @openglobus/og@0.25.5 dts
> tsc --build tsconfig.json


rober@RobertPastor MINGW64 ~/node.js/openglobus (master)


#================== npm run build mode = development ===============================

modify the package.json to run build in development mode

"scripts" : {
    "docs" : "jsdoc -r ./src/ -c ./jsdoc.conf.json -d ./docs",
    "serve_docs" : "cd docs; ws -p 8088",
    "serve" : "ws -p 3000",
    "build" : "vite build --mode development && npm run dts",

PS D:\Node.js\openglobus> npm run buildd


#=========== avoid minifying ======================

to avoid compressing minifying 

in file rollup.config.js suppress terser in the 1st plugin before the json() pluginn

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
     * Converts loaded data to segment elevation data type (colum major elevation data array in meters)
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

 