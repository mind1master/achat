$(document).ready(function() {

    var ws;

    ws = new WebSocket("ws://192.168.1.125:8888/chat");

    ws.onmessage = function(evt) {
        var data;
        data = evt.data;

        var date = new Date();        
        var time = date.getHours() + ":";
        time += ((date.getMinutes() < 10) ? "0" : "") + date.getMinutes() + ":";
        time += ((date.getSeconds() < 10) ? "0" : "") + date.getSeconds();
        time = "< " + time + ">: "
        data = time + data;
        
        $(".message:last").after("<div class=message>" + data + "<br></div>")
    };

    ws.onerror = function(e) {
        console.log(e);
    };

    function handle() {
        var message = $("#chat_message").val();
        ws.send(message);
        $("#chat_message").val("");
    }

    $("#send_message_button").click(function() {
        handle();
    })
    $("#chat_message").bind('keypress', function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) { //Enter keycode
            handle();
        }
    });
});