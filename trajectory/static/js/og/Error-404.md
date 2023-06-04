
On Monday, August 1, 2022 at 7:29:12 PM UTC+4

Hi Robert!

Let me explain why you have got 404 error. All terrain data stored as files replica of mercator grid, the same way as an ordinary tile for openstreetmap for instance. Obviously there is no file  srtm3.openglobus.org/3/5/3.ddm it means that there is no data for terrain in the coordinates z=3, y=5, x=3, where z is zoom level, and x, y - mercator grid coordinates. Zoom level defines the level grid size as 2^zoom x 2^zoom, for example zoom = 1, grid size = 2x2, zoom=2, gridsize 4x4, zoom=3, grid size 2^3x2^3 etc. In openglobus case it means that terrain provider throw an error during fetching terrain data for 3,5,3 tile index, and browser console shows a red line. If you got stuck rendering or something doesn'
t work because of 404 error for such terrain data let's try to solve it, but we need more information, I'd recommend you use source code as it is, without compiled library. but in other case it's ok:)

For kml patch, feel free to create pull request in github, that we could see the difference.

P.S. if you don't need terrain you can always set EmptyTerrain provider, check the example: http://openglobus.org/examples/emptyTerrain/emptyTerrain.html


Cheers,

Zemledelec.