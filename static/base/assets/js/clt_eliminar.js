$(document).ready(function() {
    $('.loader').hide();
});

$(document).on('click','.eliminar_cliente',function() {	
	var cliente = $(this).attr('data-cliente');
	var nombres = $(this).attr('data-nombres');
	data={
		'cliente': cliente
	}
	$("#modal_eliminarcliente .nombre_cliente").text(nombres);
	$("#modal_eliminarcliente .id_cliente_eliminar").val(cliente);
    $('#modal_eliminarcliente').modal('show');
})


$("#modal_eliminarcliente .delete_cliente").click(function ()
{
	var cliente = $("#modal_eliminarcliente .id_cliente_eliminar").val();
	var parametros = {
			"cliente": cliente,
        };
    eliminar_cliente(parametros);
    
})



function eliminar_cliente(parametros)
{
	$.ajax({
		url: '/clientes/clientes/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
                $('#modal_eliminarcliente').modal('hide');
                document.location.href='/clientes/clientes/lista';
                $('.loader').hide();                
			}else if(data.estado==2){
				$('#modal_eliminarcliente').modal('hide');
				toastr.error("Cliente no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Cliente No existe.",'Error');
			}
		}

	})

}

