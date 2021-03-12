$(document).ready(function(){
    $('.loader').hide();
})

// eliminar precio_definido

$(document).on('click', '.eliminar_alianza', function(){
    var sku = $(this).attr('data-alianza');
    var descripcion = $(this).attr('data-descripcion');
    data = {
        'sku': sku
    }
    $('#modal_eliminaralianza .nombre_alianza').text(descripcion);
    $('#modal_eliminaralianza .id_alianza_eliminar').val(sku);

    $('#modal_eliminaralianza').modal('show');
})

$("#modal_eliminaralianza .delete_alianza").click(function ()
{
	var alianza_id = $("#modal_eliminaralianza .id_alianza_eliminar").val();
	var parametros = {
			"alianza": alianza_id,
        };
    eliminar_alianza(parametros);
    
})


function eliminar_alianza(parametros)
{
	$.ajax({
		url: '/catalogo/alianzas/ajax/aliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Alianzas Eliminada', 'Eliminar');
                $('#modal_eliminaralianza').modal('hide');
                $('.loader').hide();
                location.replace('/catalogo/alianzas/lista');
			}else if(data.estado==2){
				$('#modal_eliminaralianza').modal('hide');
				toastr.error("Alianzas no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Alianza No existe",'Error');
			}
		}

	})

}
