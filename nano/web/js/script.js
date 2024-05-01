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
        sleepEvent();
    }
});
document.getElementById('sleep-overlay').addEventListener('click', function (event) {
    if (event.target === this) {
        wakeEvent();
    }
});
eel.expose(loginEvent)
function loginEvent(userData) {
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    timeoverlay.classList.remove('show'); 
    sleepoverlay.classList.remove('show');
    const obj = JSON.parse(userData)
    updateHTML(obj)
    
}
function updateHTML(dataOBJ){
    document.getElementById('greeting_header').innerText = "Welcome, "+ dataOBJ[0].NAME;
    document.getElementById('temp').innerText = dataOBJ[0].TEMP+"°";
    document.getElementById('cond').innerText = dataOBJ[0].CONDITION;
    document.getElementById('hum').innerText = dataOBJ[0].HUMIDITY;
    document.getElementById('uv').innerText = dataOBJ[0].UV_INDEX;

    document.getElementById('hr').innerText = dataOBJ[0].HEART;
    document.getElementById('cal').innerText = dataOBJ[0].CALORIES;
    document.getElementById('steps').innerText = dataOBJ[0].STEPS;
    document.getElementById('dist').innerText = dataOBJ[0].DISTANCE_WALKED;
}


eel.expose(updateEvent)
function updateEvent(userData) {
    const obj = JSON.parse(userData)
    updateHTML(obj)
    
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
    sleepoverlay.classList.remove('show');
    timeoverlay.classList.add('show');
}
