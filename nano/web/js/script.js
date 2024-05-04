// Flag to control whether to continue updating the UI with camera images
let shouldUpdate = true;

// Function to start the process of taking pictures using the camera overlay
eel.expose(startPicTaking)
function startPicTaking(){
    shouldUpdate = true;
     // Display the camera overlay and remove other overlays
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    var camoverlay = document.getElementById('camera-overlay');
    sleepoverlay.classList.remove('show');
    timeoverlay.classList.remove('show');
    camoverlay.classList.add('show');
    // Begin updating the camera feed
    updateImage();
}
// Function to stop picture taking and revert to the sleep overlay
function stopPicTaking(){
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    var camoverlay = document.getElementById('camera-overlay');
    // Hide the camera overlay and display the sleep overlay
    sleepoverlay.classList.add('show');
    timeoverlay.classList.remove('show');
    camoverlay.classList.remove('show');
    // Send signal to Python backend to stop sending pictures
    eel.stopCreating() 
}
// Function to update the UI with camera images
async function updateImage() {
    if (!shouldUpdate) {
        return;
    }
    // Request image from the backend
    const image = await eel.get_image()();
    if (!image) {
        // Stop updates if all required pictures have been taken
        shouldUpdate = false;
        stopPicTaking();
        return;
    }
    // Function to stop updating the UI with camera images
    document.getElementById('live-feed').src = image;
    // Request the next image after a short delay
    setTimeout(updateImage, 10); 
}

// python forcing display to stop updating
eel.expose(stopUpdates)
function stopUpdates() {
    shouldUpdate = false;
}


// Function triggered upon user login, updating the UI with user data
eel.expose(loginEvent)
function loginEvent(userData) {
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    timeoverlay.classList.remove('show'); 
    sleepoverlay.classList.remove('show');
    const obj = JSON.parse(userData)
    updateHTML(obj)
    
}

// Function to update the UI with user data
function updateHTML(dataOBJ){
    document.getElementById('greeting_header').innerText = "Welcome, "+ dataOBJ[0].NAME;
    document.getElementById('temp').innerText = dataOBJ[0].TEMP+"°";
    document.getElementById('indtemp').innerText = dataOBJ[0].INDOORTEMP;
    document.getElementById('cond').innerText = dataOBJ[0].CONDITION;
    document.getElementById('hum').innerText = dataOBJ[0].HUMIDITY;
    document.getElementById('uv').innerText = dataOBJ[0].UV_INDEX;

    document.getElementById('hr').innerText = dataOBJ[0].HEART;
    document.getElementById('cal').innerText = dataOBJ[0].CALORIES;
    document.getElementById('steps').innerText = dataOBJ[0].STEPS;
    document.getElementById('dist').innerText = dataOBJ[0].DISTANCE_WALKED;
}

// Function triggered to update the UI with received user data
eel.expose(updateEvent)
function updateEvent(userData) {
    const obj = JSON.parse(userData)
    updateHTML(obj)
    
}

// Function triggered to display a sleep overlay
eel.expose(sleepEvent)
function sleepEvent() {
    var timeoverlay = document.getElementById('overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    var camoverlay = document.getElementById('camera-overlay');
    sleepoverlay.classList.add('show');
    timeoverlay.classList.remove('show');
    camoverlay.classList.remove('show');



}
// Function triggered to display a screensaver overlay
eel.expose(wakeEvent)
function wakeEvent() {
    var timeoverlay = document.getElementById('overlay');
    var camoverlay = document.getElementById('camera-overlay');
    var sleepoverlay = document.getElementById('sleep-overlay');
    sleepoverlay.classList.remove('show');
    timeoverlay.classList.add('show');
    camoverlay.classList.remove('show');

}
