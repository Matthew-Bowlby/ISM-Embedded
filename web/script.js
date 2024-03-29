function getDate() {
    var now = new Date();
    var hours = now.getHours() % 12 || 12;
    var time = hours + ':' + now.getMinutes() + ":" + now.getSeconds();
    document.getElementById('time').innerHTML = time;
    eel.my_function(1, 2);
    setTimeout(getDate, 500);
}
;
getDate();
