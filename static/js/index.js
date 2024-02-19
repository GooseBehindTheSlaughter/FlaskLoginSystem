// Connect a socket to the current site
var socket = io.connect("http://" + document.domain + ":" + location.port);

function update(data) {
    document.getElementById("randomNumber").innerHTML = data.number;
    console.log(data);
};
socket.on("update_number",update); // Bind the event "##" to call "##"

// Call ## ever #
setInterval(function() {
    socket.emit('update_number');
}, 1000);  // Every 5 seconds