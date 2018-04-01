

var datos_recibidos=[];
var n_muestras=20;

var tamanho='';
var datos_recibidos_copia=[]
/*Inicializa la pantalla con todos los resultados encontrados*/
function mostrarResultados(datos){
  datos_recibidos=datos;
  datos_recibidos_copia=datos
  visualiza_filas (0 , n_muestras);
  paginatorBar(1,5,datos_recibidos.length);
  tamanho=datos_recibidos.length;
}
/*Muestra por pantalla los resultados en función de la bd*/
function orbenarPorBD(bd){
    var datos=[];
    if(bd != 'none'){
      for (var index = 0; (index < datos_recibidos_copia.length); index++) {
        if(bd==datos_recibidos_copia[index]['bd']){
          datos.push(datos_recibidos_copia[index]);
        }
      }
      datos_recibidos=datos;
    }else{
      datos_recibidos=datos_recibidos_copia;
    }
    visualiza_filas (0 , n_muestras);
    paginatorBar(1,5,datos_recibidos.length);
    tamanho=datos_recibidos.length;
}


/*Función encargada de mostrar los resultados*/
function visualiza_filas (inicio, fin) {
   $(function () {
        var content = '';


        //content += '<tbody>'; -- **superfluous**finf
          for (var index = inicio; (index < datos_recibidos.length) && (index < fin) ; index++) {
            if(datos_recibidos[index]['bd'] == 'ncbi_gds' ){
                content += '<tr bgcolor="#5DADE2">'
              }else{
          content += '<tr bgcolor="#82E0AA">'
        }
        /*content += '<td id=celda>'+datos_recibidos[index]['id'];
  content+='</td>';*/
        content += '<td id=celda onclick="seeExpedient('+index+')">'+datos_recibidos[index]['accession'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['name'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['n_samples'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['releasedate'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['especie'];
  content+='</td>';
        content += '<td>'+datos_recibidos[index]['tipoexperimento'];
  content+='</td>';
        content += '<td id="description" onclick="descriptionText('+index+')">Click to see the description'
  content+='<span></span></td>';
        content += '<td>'+datos_recibidos[index]['bd'];
  content+='</td>';
        content += '<td > <a id="enlace" onclick="descarga('+index+')">'
  content+='<img style="float:left; position:relative; left:30%"  src="/static/carpeta.png">'
  content+='</a>';
  content+='</td>';
        content += '</tr>';
          }
        $("#acrylic tbody").html(content);
   });
};
function seeExpedient(index){

  var data=JSON.stringify({"accession":datos_recibidos[index]['accession'], "file": datos_recibidos[index] })
  document.getElementById("myInput").value = data;
  document.forms["formularioExpediente"].submit();
}
function orderByDate(order){
  if(order == 'descending'){
    datos_recibidos.sort(function(a, b){return new Date(a.releasedate)-new Date(b.releasedate)});
  }else{
    datos_recibidos.sort(function(a, b){return new Date(b.releasedate)-new Date(a.releasedate)});
  }
  visualiza_filas (0 , n_muestras);
  paginatorBar(1,5,datos_recibidos.length);
  tamanho=datos_recibidos.length;
};
function orderByTecnology(){
  datos_recibidos.sort(function(a, b){
        var x = a.tipoexperimento.toLowerCase();
        var y = b.tipoexperimento.toLowerCase();
        if (x < y) {return -1;}
        if (x > y) {return 1;}
        return 0;
    });
  visualiza_filas (0 , n_muestras);
  paginatorBar(1,5,datos_recibidos.length);
  tamanho=datos_recibidos.length;
};
function orderBySpecie(){
  datos_recibidos.sort(function(a, b){
        var x = a.especie.toLowerCase();
        var y = b.especie.toLowerCase();
        if (x < y) {return -1;}
        if (x > y) {return 1;}
        return 0;
    });
  visualiza_filas (0 , n_muestras);
  paginatorBar(1,5,datos_recibidos.length);
  tamanho=datos_recibidos.length;
};
  function abrirCarpetaDescarga(elem){
      enlace=elem.id;
      res=enlace.split("/")
      res=res.slice(0,10)
      res=res.join('/')
      window.open(res);
  };
  function descarga(index){
      var enlace=datos_recibidos[index]['descarga'];
    window.open(enlace);
  };
  function descriptionText(index){
    var description_text='';
    description_text=datos_recibidos[index]['description'];
    $("tbody tr #description").click(
      function(e)
      {
        $("#myModal").modal();//llamamos a la clase modal
        $(".modal-body p").empty();//Vacia el contenido de p
        $(".modal-body p").append(description_text);//rellenamos el parrafo
      });
  };
 function enviarFTP(elem){
  /*
  enlace=elem.id;
   var url="{% url 'descargaFTP' %}";
  $.ajax({
  // la URL para la petición
  url : url ,
  data : { 'enlace' : enlace },
  type : 'POST',
  dataType : 'json',
  success : function(data) {
      alert("comenzando la descarga")
  },

  error : function(xhr, status) {
      alert('No se pudo establecer conexión');
  }
 });});
*/
};
$(document).ready(function(){

$('#myTable').pageMe({pagerSelector:'#myPager',showPrevNext:true,hidePageNumbers:false,perPage:4});

});
/*inicializador del paginador*/
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

/*Función encargada de sellecionar la página deseada*/
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
  /*Paginador*/
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
                content+='<li class="active" value="'+(j+1)+'" onclick="paginador(this); paginatorBar('+(j+1)+','+(j+5)+','+tam+')"><a class="page-link" href="javascript:void(0)">'+(j+1)+'</a></li>';
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

          content+='<div class="col-4 "  style="float: right;  padding-left:2%; padding-top:0.3%>'
                content+='<div class="row">'
              content+='<input search"  id="comment" style="padding-right: 1px; width:30%; text-align:right" value='+inicio+' onkeydown="seleccionarPagina(this)"> </input>'
              content+='<span>of '+(Math.ceil(tam/n_muestras))+'</span>'
                content+='</div></div>'
            $("#paginator1 ul").html(content);//Donde inserto la estructura creada con los content
       });
     };

  /*Corrige el error CSRFToken*/
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
