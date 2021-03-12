$(document).ready(function() {
    $('.loader').hide();
});

$(document).on('click', '.eliminar_grupoempresarial', function(){
	var nombre = $(this).attr('data-nombregrupo');
	var grupo = $(this).attr('data-grupo');
	data={
		'grupo' : grupo
	}
	$("#modal_eliminargrupo .nombre_grupo").text(nombre);
	$("#modal_eliminargrupo .id_grupo_eliminar").val(grupo);
	$('#modal_eliminargrupo').modal('show');
})


$("#modal_eliminargrupo .delete_grupo").click(function ()
{
	var grupo = $("#modal_eliminargrupo .id_grupo_eliminar").val();
	var parametros = {
			"grupo":grupo,
        };
	eliminar_grupo(parametros);
	// alert(parametros["grupo"]);
})





function eliminar_grupo(parametros)
{
	$.ajax({
		url: '/establecimientos/gruposempresariales/ajax/eliminargrupo/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Grupo Eliminado', 'Eliminar');
				obtener_grupos()
				$('#modal_eliminargrupo').modal('hide');
			}else if(data.estado==2){
				$('#modal_eliminargrupo').modal('hide');
				toastr.error("Un usuario asignado al Grupo Empresarial.",'Error');
			} 
			else{
				toastr.error("Grupo No existe",'Error');
			}
		}

	})

}



function obtener_grupos(){
  $.ajax({
    type: 'GET',
    url: '/establecimientos/gruposempresariales/ajax/obtenergrupos/',

    beforeSend: function () {
      	$('.loader').show();
    },
    success: function (response) {
		$('#contenido_grupos').html(response.grupos_html); 
		$('[data-toggle="tooltip"]').tooltip();
		$('.loader').hide();
    }
  });
  
}