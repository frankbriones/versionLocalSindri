$(document).ready(function() {
    $('.loader').hide();
});

$(document).on('click','.eliminar_tienda',function() {	
	var tienda = $(this).attr('data-tienda');
	var nombre = $(this).attr('data-descripcion');
	data={
		'tienda':tienda
	}
	$("#modal_eliminartienda .nombre_tienda").text(nombre);
	$("#modal_eliminartienda .id_tienda_eliminar").val(tienda);
    $('#modal_eliminartienda').modal('show');
})


$("#modal_eliminartienda .delete_tienda").click(function ()
{
	var tienda = $("#modal_eliminartienda .id_tienda_eliminar").val();
	var parametros = {
			"tienda":tienda,
        };
	eliminar_tienda(parametros);
})



function eliminar_tienda(parametros)
{
	$.ajax({
		url: '/establecimientos/tiendas/ajax/eliminartienda/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Tienda Eliminada', 'Eliminar');
				obtener_tiendas()
				$('#modal_eliminartienda').modal('hide');
			}else if(data.estado==2){
				$('#modal_eliminartienda').modal('hide');
				toastr.error("Un usuario asignado a la tienda.",'Error');
			}else if(data.estado==3){
				$('#modal_eliminartienda').modal('hide');
				toastr.success("Tiendas Eliminadas del usuairo.",'Listo');
			} 
			else{
				toastr.error("Tienda no existe",'Error');
			}
		}

	})

}


function obtener_tiendas(){
  $.ajax({
    type: 'GET',
    url: '/establecimientos/tiendas/ajax/obtenertiendas/',

    beforeSend: function () {
      	$('.loader').show();
    },
    success: function (response) {
		// $('#contenido_tiendas').html(response.tiendas_html); 
		// $('[data-toggle="tooltip"]').tooltip();
		// $('.loader').hide();
		// console.log(response);
		$('.loader').hide();
		document.location.href='/establecimientos/tiendas/lista';
		
		

    }
  });
  
}


