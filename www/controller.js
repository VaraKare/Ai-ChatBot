

$(document).ready(function (){
eel.expose(DisplayMessage)
eel.expose(ShowHood)
eel.expose(senderText)
eel.expose(receiverText)
//Display speak message
  
    function DisplayMessage(message){
        $('.siri-message li:first').text(message);
        $('.siri-message').textillate('start')
        console.log("DisplayMessage function exposed to Python and called with message:", message);
    }

    //Display hood
    function ShowHood(){
        document.getElementById("Oval").hidden = false;
        document.getElementById("SiriWave").hidden = true;
    }
    
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
            </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }
});