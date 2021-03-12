$(document).ready(function(){
    $('.loader').hide();
})

// eliminar taller

$(document).on('click', '.eliminar_taller', function(){
    var taller = $(this).attr('data-taller');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'taller': taller
    }
    $('#modal_eliminartaller .nombre_taller').text(nombre);
    $('#modal_eliminartaller .id_taller_eliminar').val(taller);

    $('#modal_eliminartaller').modal('show');
})

$("#modal_eliminartaller .delete_taller").click(function ()
{
	var taller_id = $("#modal_eliminartaller .id_taller_eliminar").val();
	var parametros = {
			"taller": taller_id,
        };
    eliminar_taller(parametros);
    
})


function eliminar_taller(parametros)
{
	$.ajax({
		url: '/establecimientos/talleres/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Taller Eliminado', 'Dato Eliminado');
                $('#modal_eliminartaller').modal('hide');
                document.location.href='/establecimientos/talleres/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminartaller').modal('hide');
				toastr.error("Taller  no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Taller No existe",'Error');
			}
		}

	})

}


