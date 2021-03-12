$(document).ready(function() {
    $('.loader').hide();
});
// asignar y quitar zonas a usuario

$('#id_zona').on("change", function(){
    // $('#id_lista_tiendas').show();
    var zona = document.getElementById("id_zona").value;
    var usuario = document.getElementById("usuario_idd").value;
    var parametros = {
			"zona":zona,
			"usuario": usuario
        };
    // console.log(usuario);
	tiendas_zonal(parametros);


});




function tiendas_zonal(parametros){

	$.ajax({
		type: 'GET',
		url: '/usuarios/usuario/ajax/tiendaszonal/',
		data: parametros,

		beforeSend: function () {
      	$('.loader').show();      //AlertaEspera("Guardando nota Grupal..");
	    },
	    success: function (response) {
	  //   	$('#id_lista_tiendas').show();
	  //   	let lista_disponibles = $('#id_tiendas_disponibles');
	  //   	lista_disponibles.empty();
	  //   	let li = response.tiendas_html
			// // $('#id_tiendas_disponibles').html(response.tiendas_html);
			// lista_disponibles.append(li);

			if(response.estado==1){
				toastr.success('tiendas disponibles', 'Mensaje');
			}else if(response.estado==2){
				toastr.error('tiendas ya estan asignadas', 'Error');
			}
			else{
				toastr.error('Elija una zona valida.', 'Error');
				$('.loader').hide();
			}

			$('.loader').hide();

    }

	});
}
