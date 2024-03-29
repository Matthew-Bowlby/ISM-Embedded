function getDate() {
    var now = new Date();
    var hours = now.getHours() % 12 || 12;
    var time = hours + ':' + now.getMinutes() + ":" + now.getSeconds();
    document.getElementById('time').innerHTML = time;
    setTimeout(getDate, 500);
}
;
getDate();
eel.expose(hideTime)
function hideTime() {
    // $("#time").hide()
}


// Function to toggle the overlay
function toggleOverlay() {
    var overlay = document.getElementById('overlay');
    overlay.classList.toggle('show');
}

// Close the overlay when clicking anywhere on it
document.getElementById('overlay').addEventListener('click', function (event) {
    if (event.target === this) {
        toggleOverlay();
    }
});

eel.expose(loginEvent)
function loginEvent() {

}

eel.expose(sleepEvent)
function sleepEvent() {
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    sleepoverlay.classList.add('show');
    timeoverlay.classList.remove('show');

}

eel.expose(wakeEvent)
function wakeEvent() {
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    timeoverlay.classList.add('show');
    sleepoverlay.classList.remove('show');
}
