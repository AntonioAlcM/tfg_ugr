

var datos_recibidos;
var n_muestras=20;
var description_text;
var tamanho='';

function setVariables(datos, tam){

  datos_recibidos=datos;
  tamanho=tam;
}

 function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
};
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});
function visualiza_filas (inicio, fin) {
   $(function () {
        var content = '';


        //content += '<tbody>'; -- **superfluous**finf
          for (var index = inicio; (index < datos_recibidos.length) && (index < fin) ; index++) {
        content += '<tr>'
        content += '<td id=celda>'+datos_recibidos[index]['id'];
  content+='</td>';
        content += '<td id=celda>'+datos_recibidos[index]['accession'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['name'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['muestras'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['releasedate'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['especie'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['tipoexperimento'];
  content+='</td>';
        content += '<td id="description" onclick="descriptionText('+index+')"> Click to see the description'
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['bd'];
  content+='</td>';
        content += '<td> <a id="enlace" onclick="descarga('+index+')">'
  content+='<img class="center-block" src="/static/carpeta.png">'
  content+='</a>';
  content+='</td>';
        content += '</tr>';
          }
        $("#acrylic tbody").html(content);
   });


};
 function enviarFTP(){
   enlace=document.getElementById("enlace").text;
   /*var url =
   $.ajax({
  // la URL para la petición
  url : url,
  data : { enlace : enlace },
  type : 'POST',
  dataType : 'json',
  success : function(json) {
      alert("comenzando la descarga")
  },

  error : function(xhr, status) {
      alert('No se pudo establecer conexión');
  }
});*/
};
$(document).ready(function(){

$('#myTable').pageMe({pagerSelector:'#myPager',showPrevNext:true,hidePageNumbers:false,perPage:4});

});

  function paginador(element){
      var fila_inicio=element.value;
      fila_inicio=fila_inicio*n_muestras;
      visualiza_filas(fila_inicio-n_muestras, fila_inicio);
  };
  function isAlphabetic(cadena)
{
      if (cadena.match(/^[a-zA-Z]+$/))
      {
        return true;
      }
      else
      {
        return false;
      }
}


  function seleccionarPagina(element){
      if(event.key === 'Enter') {
          var fila_inicio=element.value;
          var tiene_caracteres=false;
          for(var i=0; i < fila_inicio.length && tiene_caracteres==false ; i++){
            if(isAlphabetic(fila_inicio.charAt(i))){
              tiene_caracteres=true;
            }
          }
          if(tiene_caracteres){
            alert("Introduzca un número entre 1 y "+ tope );
          }else{
          var inicio=parseInt(fila_inicio)
          var tope=Math.ceil(tamanho/n_muestras);
          var fin=inicio+5;
          if(inicio>tope || inicio<1){
            alert("Introduzca un número entre 1 y "+ tope );
          }else{
            if(inicio+5>tope){
              fin=tope-inicio;
            }
            paginatorBar(inicio,fin,tamanho)
            fila_inicio=fila_inicio*n_muestras;
            visualiza_filas(fila_inicio-n_muestras, fila_inicio);
          }
        }
      }

  };
  function paginatorBar(inicio,fin,tam) {

       $(function () {

            if(inicio<Math.ceil(tam/n_muestras) && inicio>Math.ceil(tam/n_muestras)-5){
                fin=Math.ceil(tam/n_muestras);
            }
            if(fin> Math.ceil(tam/n_muestras))
              fin= Math.ceil(tam/n_muestras)
            var content = '';
            if(inicio>1){
              content+=	'<li class="active" onclick="paginatorBar('+1+','+5+','+tam+') ; paginador(this);"  value="'+1+'"><a class="page-link" href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">«</span></a>'
            }else{
              content+=	'<li class="disabled"><a class="page-link" href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">«</span></a>'
            }
            if(inicio>1){
              content+=	'<li class="active" onclick="paginatorBar('+(inicio-1)+','+(fin-1)+','+tam+'); paginador(this);"  value="'+(inicio-1)+'"><a class="page-link" href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">‹</span></a>'
            }else{
              content+=	'<li class="disabled"><a class="page-link" href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">‹</span></a>'
            }
              for (var j=inicio-1; j<(fin || Math.ceil(tam/n_muestras)); j++) {
                content+='<li class="active" value="'+(j+1)+'" onclick="paginador(this)"><a class="page-link" href="javascript:void(0)">'+(j+1)+'</a></li>';
              }
          if(inicio<(Math.ceil(tam/n_muestras))){
            content+='<li class="active" value="'+(inicio+1)+'" onclick="paginatorBar('+(inicio+1)+','+(fin+1)+','+tam+'); paginador(this); "><a class="page-link" href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">›</span></a></li>'
          }else{
            content+='<li class="disabled" value="'+(inicio+1)+'" ><a class="page-link" href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">›</span></a></li>'
          }
          if(inicio<(Math.ceil(tam/n_muestras))){
            content+='<li class="active" value="'+(Math.ceil(tam/n_muestras))+'"onclick="paginatorBar('+Math.ceil(tam/n_muestras)+','+Math.ceil(tam/n_muestras)+','+tam+'); paginador(this);"><a class="page-link" href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
          }else{
            content+='<li class="disabled" value="'+(fin)+'"><a class="page-link" href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
          }

          content+='<div class="col-xs-4 "  style="float: right;">'
                content+='<div class="row">'
              content+='<input class="col-sm-2 search" rows="1s" id="comment" style="padding-right: 1px" value='+inicio+' onkeydown="seleccionarPagina(this)"> </input>'
              content+='<span class="col-sm-4" style="width:auto">of '+(Math.ceil(tam/n_muestras))+'</span>'
                content+='</div></div>'
            $("#paginator1 ul").html(content);//Donde inserto la estructura creada con los content
       });
     };
  function abrirCarpetaDescarga(){
      enlace=document.getElementById("enlace").text;
      windows.open(enlace, '_blank');
  };
  function descarga(index){
      var enlace=datos_recibidos[index]['descarga'];
    window.open(enlace);
  };
  function descriptionText(index){
    description_text=datos_recibidos[index]['description'];
    $("tbody tr td ").click(
      function(e)
      {
        $("#myModal").modal();//llamamos a la clase modal
        $(".modal-body p").empty();//Vacia el contenido de p
        $(".modal-body p").append(description_text);//rellenamos el parrafo
      });
  };
