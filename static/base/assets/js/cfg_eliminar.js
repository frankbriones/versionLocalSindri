$(document).ready(function() {
    $('.loader').hide();
});

$(document).on('click','.eliminar_rubro',function() {	
	var rubro = $(this).attr('data-rubro');
	var nombre = $(this).attr('data-descripcion');
	data={
		'rubro':rubro
	}
	$("#modal_eliminarrubro .nombre_rubro").text(nombre);
	$("#modal_eliminarrubro .id_rubro_eliminar").val(rubro);
    $('#modal_eliminarrubro').modal('show');
})


$("#modal_eliminarrubro .delete_rubro").click(function ()
{
	var rubro = $("#modal_eliminarrubro .id_rubro_eliminar").val();
	var parametros = {
			"rubro": rubro,
        };
    eliminar_rubro(parametros);
    // alert(rubro);
    
})



function eliminar_rubro(parametros)
{
	$.ajax({
		url: '/configuraciones/configuracion/rubros/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Rubro Eliminado', 'Dato Eliminado');
                $('#modal_eliminarrubro').modal('hide');
                document.location.href='/configuraciones/configuracion/rubros/lista/';
                $('.loader').hide();                
			}else if(data.estado==2){
				$('#modal_eliminarrubro').modal('hide');
				toastr.error("Rubro no puede ser eliminado, esta siendo utilizado.",'Error');
			}
			else{
				toastr.error("Rubro No existe.",'Error');
			}
		}

	})

}



