
var i = 0;

function timedCount() {
    if (i < 100) {
        i = i + 1;
    } else {
        i = 1;
    }

    postMessage(i);
    setTimeout("timedCount()", 100);
}

timedCount();
