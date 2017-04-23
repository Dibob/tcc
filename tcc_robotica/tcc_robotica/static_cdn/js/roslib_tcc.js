// This function connects to the rosbridge server running on the local computer on port 9090
var rbServer = new ROSLIB.Ros({
    url : 'ws://0.tcp.ngrok.io:17483'
 });

var elem = document.querySelector('.js-switch');
var init = new Switchery(elem);


  var servo_motor = $("#hidden_servo").val();
  var ar_condicionado= $("#hidden_ar_condicionado").val();
  var radio  = $("#id_radio").val();

   $('input[type=radio]').each(function(index) {
    if($(this).val() == servo_motor || $(this).val() == ar_condicionado){
       $(this).attr('checked', 'checked');
   }
});

setTimeout(function() {
            $('.alert-success').fadeOut('slow');
  }, 4000);         
  if($("#hidden_radio").attr("value") == "True"){
        $("#id_radio").attr('checked','checked');
       }
    else{
       $('#id_radio').removeAttr('checked');
    }   

init();
$("#detectar_pessoa" ).on("click",function() {
    executarBuscaFacial();
});

$("#classificacao_button" ).on("click",function() {
    executarClassificacaoFacial();
});

$("#aplicar" ).on("click",function() {
    setarValoresArduino();
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
        serviceType : 'tcc_robotica/face_server'
    });

    var request = new ROSLIB.ServiceRequest({
        tipo: parseInt($("#tipo_algoritmo").val()), 
     });
   
    face_client.callService(request, function(result) {
       response = result.nome
       if(response == "desconhecido") {
            $(".panel-class").show();
            $(".login_jumbo").css("display","none");
        }
        else{
            $(location).attr("href", "/automotivo/perfil/"+response)
        }

   });
 }


 function executarClassificacaoFacial(){
    var face_client = new ROSLIB.Service({
        ros : rbServer,
        name : '/face_detect',
        serviceType : 'tcc_robotica/face_detect'
    });

    var request = new ROSLIB.ServiceRequest({
        tipo: parseInt($("#tipo_algoritmo").val()),
        nome : $("#nome").val()
     });
   
    face_client.callService(request, function(result) {
       valor = result.classificacao
      if(valor){
           $(location).attr("href", "/automotivo/create/"+$("#nome").val());
     }
   });
 }


 function setarValoresArduino(){
    var face_client = new ROSLIB.Service({
        ros : rbServer,
        name : '/arduino',
        serviceType : 'tcc_robotica/arduino'
    });

    var request = new ROSLIB.ServiceRequest({
        servo_angulo: parseInt(servo_motor),
        nivel_arcondicionado :parseInt(ar_condicionado),
        radio : (radio == "on"),
     });
   
    face_client.callService(request, function(result) {
       valor = result.update_servo
      if(valor){
           $(location).attr("href", "/automotivo/create/"+$("#nome").val());
     }
   });
 }






