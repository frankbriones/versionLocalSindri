$(document).ready(function() {
    $('.loader').hide();
});


$(document).on('click','.eliminar_localidad',function() {	
	var localidad = $(this).attr('data-localidad');
	var nombre = $(this).attr('data-descripcion');
	data={
		'localidad':localidad
	}
	$("#modal_eliminarlocalidad .nombre_localidad").text(nombre);
	$("#modal_eliminarlocalidad .id_localidad_eliminar").val(localidad);
    $('#modal_eliminarlocalidad').modal('show');
})


$("#modal_eliminarlocalidad .delete_localidad").click(function ()
{
	var localidad = $("#modal_eliminarlocalidad .id_localidad_eliminar").val();
	var parametros = {
			"localidad": localidad,
        };
    eliminar_localidad(parametros);
    
})



function eliminar_localidad(parametros)
{
	$.ajax({
		url: '/ubicaciones/localidades/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Localidad Eliminada', 'Eliminado');
				// obtener_tiendas()
                $('#modal_eliminarlocalidad').modal('hide');
                document.location.href='/ubicaciones/localidades/lista';
                $('.loader').hide();

                
			}else if(data.estado==2){
				$('#modal_eliminarlocalidad').modal('hide');
				toastr.error("Localidad asignada a una Ciudad.",'Error');
			}
			else{
				toastr.error("Localidad No existe",'Error');
			}
		}

	})

}


// eliminar zonas 



$(document).on('click','.eliminar_zona',function() {	
	var zona = $(this).attr('data-zona');
	var nombre = $(this).attr('data-descripcion');
	data={
		'zona':zona
	}
	$("#modal_eliminarzona .nombre_zona").text(nombre);
	$("#modal_eliminarzona .id_zona_eliminar").val(zona);
    $('#modal_eliminarzona').modal('show');
    console.log(zona);
})


$("#modal_eliminarzona .delete_zona").click(function ()
{
	var zona = $("#modal_eliminarzona .id_zona_eliminar").val();
	var parametros = {
			"zona": zona,
        };
    eliminar_zona(parametros);
    
})



function eliminar_zona(parametros)
{
	$.ajax({
		url: '/ubicaciones/zonas/ajax/eliminar/',
		type: 'GET',
		data: parametros,
 
		success: function(data){
			if(data.estado==1){
				toastr.success('Zona Eliminada', 'Dato Eliminado');
                $('#modal_eliminarzona').modal('hide');
                document.location.href='/ubicaciones/zonas/lista';
                $('.loader').hide();
			}else if(data.estado==2){
                $('#modal_eliminarzona').modal('hide');
				toastr.error(data.tienda+", tiene asignada la zona.",'Error');
			}
			else{
				toastr.error("Zona No existe",'Error');
			}
		}

	})

}


// eliminar ciudades



$(document).on('click','.eliminar_ciudad',function() {	
	var ciudad = $(this).attr('data-ciudad');
	var nombre = $(this).attr('data-descripcion');
	data={
		'ciudad':ciudad
	}
	$("#modal_eliminarciudad .nombre_ciudad").text(nombre);
	$("#modal_eliminarciudad .id_ciudad_eliminar").val(ciudad);
    $('#modal_eliminarciudad').modal('show');
    console.log(ciudad);
})

$("#modal_eliminarciudad .delete_ciudad").click(function ()
{
	var ciudad_id = $("#modal_eliminarciudad .id_ciudad_eliminar").val();
	var parametros = {
			"ciudad": ciudad_id,
        };
    eliminar_ciudad(parametros);
    
})



function eliminar_ciudad(parametros)
{
	$.ajax({
		url: '/ubicaciones/ciudades/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Ciudad Eliminada', 'Dato Eliminado');
                $('#modal_eliminarciudad').modal('hide');
                document.location.href='/ubicaciones/ciudades/lista';
                $('.loader').hide();
			}else if(data.estado==2){
                $('#modal_eliminarciudad').modal('hide');
				toastr.error("Ciudad no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Ciudad No existe",'Error');
			}
		}

	})

}





// eliminar sectores



$(document).on('click','.eliminar_sector',function() {	
	var sector = $(this).attr('data-sector');
	var nombre = $(this).attr('data-descripcion');
	data={
		'sector':sector
	}
	$("#modal_eliminarsector .nombre_sector").text(nombre);
	$("#modal_eliminarsector .id_sector_eliminar").val(sector);
    $('#modal_eliminarsector').modal('show');
    console.log(sector);
})

$("#modal_eliminarsector .delete_sector").click(function ()
{
	var sector_id = $("#modal_eliminarsector .id_sector_eliminar").val();
	var parametros = {
			"sector": sector_id,
        };
    eliminar_sector(parametros);
    
})



function eliminar_sector(parametros)
{
	$.ajax({
		url: '/ubicaciones/sectores/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				toastr.success('Sector Eliminado.', 'Dato Eliminado');
                $('#modal_eliminarsector').modal('hide');
                document.location.href='/ubicaciones/sectores/lista';
                $('.loader').hide();
			}else if(data.estado==2){
                $('#modal_eliminarsector').modal('hide');
				toastr.error("Sector no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Sector No existe",'Error');
			}
		}

	})

}
