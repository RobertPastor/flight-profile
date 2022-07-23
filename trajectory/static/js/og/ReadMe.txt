How to rebuild the final og after applying modifications


go to the repo and launch PowerShell

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

=================================
copy from D:\Node.js\openglobus\dist\@openglobus
1) og.umd.js
2) og.umd.js.map

to the project static js folder : /flight-profile/trajectory/static/js/og

=================================
to avoid compressing minifying 

in file rollup.config.js suppress terser in the 1st plugins

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

