// This function connects to the rosbridge server running on the local computer on port 9090
var rbServer = new ROSLIB.Ros({
    url : 'ws://0.tcp.ngrok.io:11723'
 });

init();
$("#detectar_pessoa" ).on("click",function() {
    executarBuscaFacial();
});

var template = $("#feedback");
var response = "";
 
function init()
{
   $(".panel-class").css("display","none");
    // This function is called upon the rosbridge connection event
 rbServer.on('connection', function() {
     // Write appropriate message to #feedback div when successfully connected to rosbridge
   
     template.add("<p>Connected to websocket server.</p>");
 });

// This function is called when there is an error attempting to connect to rosbridge
rbServer.on('error', function(error) {
    // Write appropriate message to #feedback div upon error when attempting to connect to rosbridge
    template.add("<p>Error connecting to websocket server.</p>");
});

// This function is called when the connection to rosbridge is closed
rbServer.on('close', function() {
    // Write appropriate message to #feedback div upon closing connection to rosbridge
    template.add("<p>Connection to websocket server closed.</p>");
 });

}

 function executarBuscaFacial(){
    var face_client = new ROSLIB.Service({
        ros : rbServer,
        name : '/face_reco',
        serviceType : 'tcc-robotica/face_server'
    });

    var request = new ROSLIB.ServiceRequest({
        tipo: 1
     });
   
    face_client.callService(request, function(result) {
       console.log('Result for service call on '
         + face_client.tipo
         + ': '
         + result.nome);
       response = result.nome
       if(response == "desconhecido") {
            $(".panel-class").show();
            $(".login_jumbo").css("display","none");
        }
        else{
            $(location).attr("href", "{% url 'perfil' perfil.id %}")
        }

   });
 }