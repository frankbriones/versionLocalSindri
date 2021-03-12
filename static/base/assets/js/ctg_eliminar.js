$(document).ready(function(){
    $('.loader').hide();
})

// eliminar precio_definido

$(document).on('click', '.eliminar_precio', function(){
    var precio = $(this).attr('data-precio');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'precio': precio
    }
    $('#modal_eliminarprecio .nombre_precio').text(nombre);
    $('#modal_eliminarprecio .id_precio_eliminar').val(precio);

    $('#modal_eliminarprecio').modal('show');
})

$("#modal_eliminarprecio .delete_precio").click(function ()
{
	var precio_id = $("#modal_eliminarprecio .id_precio_eliminar").val();
	var parametros = {
			"precio": precio_id,
        };
    eliminar_precio(parametros);
    
})


function eliminar_precio(parametros)
{
	$.ajax({
		url: '/catalogo/precios/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Precio Eliminado', 'Dato Eliminado');
				// obtener_tiendas()
                $('#modal_eliminarprecio').modal('hide');
                document.location.href='/catalogo/precios/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminarprecio').modal('hide');
				toastr.error("Precio  no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Precio No existe",'Error');
			}
		}

	})

}



// eliminar divisiones

$(document).on('click', '.eliminar_division', function(){
    var division = $(this).attr('data-division');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'division': division
    }
    $('#modal_eliminardivision .nombre_division').text(nombre);
    $('#modal_eliminardivision .id_division_eliminar').val(division);

    $('#modal_eliminardivision').modal('show');
})

$("#modal_eliminardivision .delete_division").click(function ()
{
	var division_id = $("#modal_eliminardivision .id_division_eliminar").val();
	var parametros = {
			"division": division_id,
        };
    eliminar_division(parametros);
    
})


function eliminar_division(parametros)
{
	$.ajax({
		url: '/catalogo/divisiones/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Precio Eliminado', 'Dato Eliminado');
				// obtener_tiendas()
                $('#modal_eliminardivision').modal('hide');
                document.location.href='/catalogo/divisiones/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminardivision').modal('hide');
				toastr.error("Division no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Division No existe",'Error');
			}
		}

	})

}



// eliminar Categorias

$(document).on('click', '.eliminar_categoria', function(){
    var categoria = $(this).attr('data-categoria');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'categoria': categoria
    }
    $('#modal_eliminarcategoria .nombre_categoria').text(nombre);
    $('#modal_eliminarcategoria .id_categoria_eliminar').val(categoria);

    $('#modal_eliminarcategoria').modal('show');
})

$("#modal_eliminarcategoria .delete_categoria").click(function ()
{
	var categoria_id = $("#modal_eliminarcategoria .id_categoria_eliminar").val();
	var parametros = {
			"categoria": categoria_id,
        };
    eliminar_categoria(parametros);
    
})


function eliminar_categoria(parametros)
{
	$.ajax({
		url: '/catalogo/categorias/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Categoria Eliminada', 'Dato Eliminado');
				
                $('#modal_eliminarcategoria').modal('hide');
                document.location.href='/catalogo/categorias/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminarcategoria').modal('hide');
				toastr.error("Categoria no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Categoria No existe",'Error');
			}
		}

	})

}




// eliminar Tallas

$(document).on('click', '.eliminar_talla', function(){
    var talla = $(this).attr('data-talla');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'talla': talla
    }
    $('#modal_eliminartalla .nombre_talla').text(nombre);
    $('#modal_eliminartalla .id_talla_eliminar').val(talla);

    $('#modal_eliminartalla').modal('show');
})

$("#modal_eliminartalla .delete_talla").click(function ()
{
	var talla_id = $("#modal_eliminartalla .id_talla_eliminar").val();
	var parametros = {
			"talla": talla_id,
        };
    eliminar_talla(parametros);
    
})


function eliminar_talla(parametros)
{
	$.ajax({
		url: '/catalogo/tallas/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Talla Eliminada', 'Dato Eliminado');
				
                $('#modal_eliminartalla').modal('hide');
                document.location.href='/catalogo/tallas/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminartalla').modal('hide');
				toastr.error("Talla no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Talla No existe",'Error');
			}
		}

	})

}


// eliminar color

$(document).on('click', '.eliminar_color', function(){
    var color = $(this).attr('data-color');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'color': color
    }
    $('#modal_eliminarcolor .nombre_color').text(nombre);
    $('#modal_eliminarcolor .id_color_eliminar').val(color);

    $('#modal_eliminarcolor').modal('show');
})

$("#modal_eliminarcolor .delete_color").click(function ()
{
	var color_id = $("#modal_eliminarcolor .id_color_eliminar").val();
	var parametros = {
			"color": color_id,
        };
    eliminar_color(parametros);
    
})


function eliminar_color(parametros)
{
	$.ajax({
		url: '/catalogo/colores/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Color Eliminado', 'Dato Eliminado');
				
                $('#modal_eliminarcolor').modal('hide');
                document.location.href='/catalogo/colores/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminarcolor').modal('hide');
				toastr.error("Color no puede ser eliminado.",'Error');
			}
			else{
				toastr.error("Color No existe",'Error');
			}
		}

	})

}




// eliminar Piedra

$(document).on('click', '.eliminar_piedra', function(){
    var piedra = $(this).attr('data-piedra');
    var nombre = $(this).attr('data-descripcion');
    data = {
        'piedra': piedra
    }
    $('#modal_eliminarpiedra .nombre_piedra').text(nombre);
    $('#modal_eliminarpiedra .id_piedra_eliminar').val(piedra);

    $('#modal_eliminarpiedra').modal('show');
    // console.log(nombre);
})

$("#modal_eliminarpiedra .delete_piedra").click(function ()
{
	var piedra_id = $("#modal_eliminarpiedra .id_piedra_eliminar").val();
	var parametros = {
			"piedra": piedra_id,
        };
    
    eliminar_piedra(parametros);
    
})


function eliminar_piedra(parametros)
{
	$.ajax({
		url: '/catalogo/piedras/ajax/eliminar/',
		type: 'GET',
		data: parametros,

		success: function(data){
			if(data.estado==1){
				// toastr.success('Piedra Eliminada', 'Dato Eliminado');
				
                $('#modal_eliminarpiedra').modal('hide');
                document.location.href='/catalogo/piedras/lista';
                $('.loader').hide();
			}else if(data.estado==2){
				$('#modal_eliminarpiedra').modal('hide');
				toastr.error("Piedra no puede ser eliminada.",'Error');
			}
			else{
				toastr.error("Piedra No existe",'Error');
			}
		}

	})

}