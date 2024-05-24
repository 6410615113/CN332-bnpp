var sX = 0;
var sY = 0;
var eX = 0;
var eY = 0;

var i = 0;
function getPosition(event) {
    var bounds = event.target.getBoundingClientRect();
    var x = event.clientX - bounds.left;
    var y = event.clientY - bounds.top;
    if (i % 2) {
        eX = x.toFixed(0);
        eY = y.toFixed(0);
    } else {
        sX = x.toFixed(0);
        sY = y.toFixed(0);
    }
    i++;

    setValues();
}

function setValues() {
    document.getElementById('id_start_x').value = sX;
    document.getElementById('id_start_y').value = sY;
    document.getElementById('id_end_x').value = eX;
    document.getElementById('id_end_y').value = eY;
}

const video = document.getElementById('video');
video.addEventListener('click', getPosition);