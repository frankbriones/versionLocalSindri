$(document).ready(function(){
    $('.loader').hide();
})

// eliminar precio_definido

$(document).on('click', '.eliminar_item', function(){
    var sku = $(this).attr('data-item');
    var descripcion = $(this).attr('data-descripcion');
    data = {
        'sku': sku
    }
    $('#modal_eliminar_item .nombre_item').text(descripcion);
    $('#modal_eliminar_item .id_item_eliminar').val(sku);

    $('#modal_eliminar_item').modal('show');
})

$("#modal_eliminar_item .delete_item").click(function ()
{
	var item_id = $("#modal_eliminar_item .id_item_eliminar").val();
	var parametros = {
			"item": item_id,
        };
    eliminar_alianza(parametros);
    
})


function eliminar_alianza(parametros)
{
	$.ajax({
		url: '/catalogo/items/ajax/aliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Item Eliminado', 'Eliminar');
                $('#modal_eliminar_item').modal('hide');
                $('.loader').hide();
                location.replace('/catalogo/items/lista/1');
			}else if(data.estado==2){
				$('#modal_eliminar_item').modal('hide');
				toastr.error("Item no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Item No existe",'Error');
			}
		}

	})

}
