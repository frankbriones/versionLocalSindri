$(document).ready(function(){
    $('.loader').hide();
})

// eliminar observacion

$(document).on('click', '.eliminar_observacion', function(){
    var id_obs = $(this).attr('data-obs');
    var titulo = $(this).attr('data-titulo');
    console.log(titulo)
    data = {
        'id_obs': id_obs
    }
    console.log(data)
    $('#modal_eliminarobs .nombre_obs').text(titulo);
    $('#modal_eliminarobs .id_obs_eliminar').val(id_obs);

    $('#modal_eliminarobs').modal('show');
})


$("#modal_eliminarobs .delete_obs").click(function ()
{
	var obs_id = $("#modal_eliminarobs .id_obs_eliminar").val();
	console.log(obs_id)
	var parametros = {
			"obs_id": obs_id,
        };
    eliminar_observacion(parametros);

})


function eliminar_observacion(parametros)
{
	$.ajax({
		url: '/configuraciones/observacion/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Taller Eliminado', 'Dato Eliminado');
                $('#modal_eliminarobs').modal('hide');
                document.location.href='/configuraciones/observacion/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminarobs').modal('hide');
				toastr.error("Observacion no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Taller No existe",'Error');
			}
		}

	})

}


