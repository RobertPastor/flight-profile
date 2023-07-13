
## browser freezing during layer remove

og version is 0.16.3 ?

if brower proposes to debug then lot of time spent in og following function

function spliceTypedArray(arr, starting, deleteCount, elements = []) {
        if (arr.length === 0) {
            return arr;
        }
        const newSize = arr.length - deleteCount + elements.length;
        const splicedArray = new arr.constructor(newSize);
        splicedArray.set(arr.subarray(0, starting));
        splicedArray.set(elements, starting);
        splicedArray.set(arr.subarray(starting + deleteCount), starting + elements.length);
        return splicedArray;
    }