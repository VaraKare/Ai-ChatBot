 $(document).ready
 (function (){
    // console.log("Initializing textillate...");
    $('.text').textillate({
        loop:true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });

    // siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 840,
        height: 200,
        style:"ios9",
        amplitude:"1",
        speed:"0.20",
        autostart:true,
      });

      //Siri message Animation
      $('.siri-message').textillate({
        loop:true,
        sync: true,
        in:{
            effect: "fadeInUp",
            sync:true,
        },
        out:{
            effect: "fadeOutUp",
            sync:true,
        },
    });

    //Mic button click event
    $("#MicBtn").click(function () { 
        startListening(); 
    });
    // Function to start listening for commands
    function startListening() {
        eel.platAssistantSound(); // Play assistant sound
        $("#Oval").attr("hidden", true); // Hide main text window
        $("#SiriWave").attr("hidden", false); // Show Siri wave window
        eel.allCommands()(function (response) {
            handleCommandResponse(response);
        });
    }

    function doc_keyUp(e) {
        console.log(`Key: ${e.key}, Code: ${e.code}, MetaKey: ${e.metaKey}, CtrlKey: ${e.ctrlKey}, AltKey: ${e.altKey}`);

        if (e.key.toLowerCase() === 'e' && (e.ctrlKey || e.altKey)) {
            e.preventDefault();
            console.log("Control or Alt + E detected! Starting listening...");
            startListening();
        }
    }
        document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message){
          if(message != ""){
            $("#Oval").attr("hidden", true); 
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $('#chatbox').val("")
            $("#MicBtn").attr("hidden", false); 
            $("#SendBtn").attr("hidden", true);
          }
    }
     // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }
    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
     // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });


      

    // Function to handle the response from the Python backend
    function handleCommandResponse(response) {
        console.log("Command response:", response);

        if (response === "success") {
            // If the command was successful, go back to the Siri wave window
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
        } else {
            // If the command failed or is unrecognized, go back to the main text window
            $("#Oval").attr("hidden", false);
            $("#SiriWave").attr("hidden", true);
        }
    }
    
 });