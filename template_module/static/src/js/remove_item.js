$( document ).ready(function() {

   //console.log("cambio")
   //console.log("Boton = " + $(".oe_action_button"))
  // console.log("Boton = " + $(".oe_action_button").length)
   
   
   validar_boton();

});

 function remover_item(){
 $("body").append("<div  id='loading_div' style='width: 100%;background-color:black;opacity:0.5;min-height: 100%;height: auto !important;position: fixed;top:0;left:0;'></div>")
 setTimeout(function(){ 
   var list = document.getElementsByClassName("ui-sortable")[0];
  // console.log(list)
 if(list == "")
 {
    console.log("no encontrado")
   remover_item()
}
else
{
   remover_item_final()
}
  }, 1000);
 }

 function remover_item_final(){
  // alert("termino");

   setTimeout(function() {
      $("#loading_div").remove();
      var list = document.getElementsByClassName("ui-sortable")[0];
     // console.log("lista: " + list);
      list.removeChild(list.childNodes[0]);
     // console.log('Esta funcionando');
      //   location.reload();
   }, 3500);
    
}

function validar_boton() {
   setTimeout(function(){
   var boton = $(".oe_action_button").length;
   if (boton <= 0) {
      //console.log("No se Encuentra!")
      validar_boton()
   }
   else {
      $(".oe_action_button").attr("onclick","llamar_boton()");
   }
   },500)
   
}

function llamar_boton() {
   ///alert("TEST_1234");         
   setTimeout(function(){ 
      //.log($("button[name*='search_visitor']"));
      $("button[name*='search_visitor']").attr("onclick","remover_item()");
   }, 4000);
}