$(document).ready(function() {
    $('.loader').hide();
});


$(document).on('click','.eliminar_proveedor',function() {	
	var proveedor = $(this).attr('data-proveedor');
	var nombre = $(this).attr('data-descripcion');
	data={
		'proveedor':proveedor
	}
	$("#modal_eliminarproveedor .nombre_proveedor").text(nombre);
	$("#modal_eliminarproveedor .id_proveedor_eliminar").val(proveedor);
    $('#modal_eliminarproveedor').modal('show');
})


$("#modal_eliminarproveedor .delete_proveedor").click(function ()
{
	var proveedor_id = $("#modal_eliminarproveedor .id_proveedor_eliminar").val();
	var parametros = {
			"proveedor": proveedor_id,
        };
    eliminar_proveedor(parametros);
    
})



function eliminar_proveedor(parametros)
{
	$.ajax({
		url: '/proveedores/proveedores/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Proveedor Eliminado', 'Dato Eliminado');
				// obtener_tiendas()
                $('#modal_eliminarproveedor').modal('hide');
                document.location.href='/proveedores/proveedores/lista';
                $('.loader').hide();

                
			}else if(data.estado==2){
				$('#modal_eliminarproveedor').modal('hide');
				toastr.error("Proveedor  no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Proveedor No existe",'Error');
			}
		}

	})

}