$(document).ready(function(){
	$('.loader').hide();
})


var peso_solicitado = 0;
var gramos_base = 0;
var unidades_solicitadas = 1;
var externa = ('{{ solicitud.externa }}'.toLowerCase() === 'true');

// valores taller
var costo_gramo_base_ta = parseFloat('{{ configuracion_ta.costo_gramo_base }}'.replace(/,/, '.'));
var precio_gramo_base_ta = parseFloat('{{ configuracion_ta.precio_gramo_base }}'.replace(/,/, '.'));
var prct_utilidad_base_ta = parseFloat('{{ configuracion_ta.utilidad_sobre_base }}'.replace(/,/, '.'));
var costo_base_total_taller = 0;
var utilidad_base_ta = 0;
var precio_base_total_taller = 0;
var costo_unitario_tar = parseFloat('{{ solicitud.costo_fabricacion_unitario }}'.replace(/,/, '.'));
var costo_total_fabricacion_taller = 0;
var prct_util_fabricacion_taller = parseFloat('{{ configuracion_ta.utilidad_sobre_fabricacion }}'.replace(/,/, '.'));
var utilidad_fabricacion_taller = 0;
var precio_fabricacion_unitario = parseFloat('{{ solicitud.precio_fabricacion_unitario }}'.replace(/,/, '.'));
var precio_fabricacion_total_ta = 0;
var total_rubros = parseFloat('{{ solicitud.total_rubros }}'.replace(/,/, '.'));
var subtotal_taller = 0;
var impuestos_taller = 0;
var total_taller = 0;
var prct_impuestos_taller = parseFloat('{{ configuracion_ta.prct_impuestos }}'.replace(/,/, '.'));
if (externa){
    prct_impuestos_taller = parseFloat('{{ solicitud.prct_impuestos_ta }}'.replace(/,/, '.'));
}


// valores joyería
// var costo_gramo_base_op = parseFloat('{{ configuracion.costo_gramo_base }}'.replace(/,/, '.'));
// var precio_gramo_base_op = parseFloat('{{ configuracion.precio_gramo_base }}'.replace(/,/, '.'));
var costo_base_total_op = 0;
// var prct_utilidad_base_op = parseFloat('{{ configuracion_op.utilidad_sobre_base }}'.replace(/,/, '.'));
var utilidad_base_op = 0;
var precio_base_total_op = 0;
// var prct_util_fabricacion_op = parseFloat('{{ prct_util_fabricacion_op }}'.replace(/,/, '.'));
// var precio_unitario_op = parseFloat('{{ precio_unitario_op }}'.replace(/,/, '.'));
var utilidad_fabricacion_op = 0;
var precio_fabricacion_total_op = 0;
var subtotal_op = 0;
var impuestos_op = 0;
var total_fabricacion_op = 0;
var subtotal_transaccion = 0;
// var prct_impuestos_joyeria = parseFloat('{{ configuracion_op.prct_impuestos }}'.replace(/,/, '.'));
var impuestos_solicitud = 0;
var precio_sistema = 0;
var descuento = 0;
var precio_final_solicitud = 0;

// valores piedras
// let piedrasLista;
let costoTotalPiedrasOperaciones = 0;
// let precioTotalPiedrasTa = '{{precio_total_piedras_taller}}' ? parseFloat('{{precio_total_piedras_taller}}'.replace(/,/, '.')) : 0;
// // let costoTotalPiedraOp = parseFloat('{{costo_total_piedras_op}}');
// let utilidadTotalPiedrasOp = parseFloat('{{ utilidad_piedras_op }}'.replace(/,/, '.'));
// let precioTotalPiedrasOp parseFloat('{{precio_total_piedras_op}}'.replace(/,/, '.'));
// let imp_piedras = 0;



// // valores adicionales
// let adicionales_lista;
let costoTotalAdicionalesTaller = 0;
// let precioTotalAdicionalesTa = '{{precio_total_adicionales_taller}}' ? parseFloat('{{precio_total_adicionales_taller}}'.replace(/,/, '.')) : 0;
// // let costoTotalPiedraOp = parseFloat('{{costo_total_piedras_op}}');
// let utilidadTotalAdicionalesOp = parseFloat('{{ utilidad_adicionales_op }}'.replace(/,/, '.'));
var precioTotalAdicionalesOp = 0;
// var precioTotalAdicionalesTaller =0;
// let imp_adicionales = 0;
let precio_totalAdiOp = 0;
// let utilidadTotalPiedrasOp = 0;
let costo_color_unitario = 0;



// valores taller formula inversa

function calcularValoresTallerInversa(peso, unidades, origen_material){
	if(tipo_catalogo === 'PRODUCTOS'){
		if(item_categoria === 'UNIDAD'){
			costo_color_unitario = 0;
			tipo_transaccion = 2;
		}else{
			id_color = $('#id_color').val();
			if (id_color === '0') {
			    mensaje("Debe escoger un color", 'orange');
			    $('#id_color').addClass('select-error');
			    return;
			}else {
				if(costo_color_unitario !== 0){

                	costo_color_unitario = parseFloat($('option:selected', '#id_color').attr('costo').replace(/,/, '.'));
				}
            }

            tienda_sociedad = ($('#id_tienda').val());
            if(origen_material === 'JOYERIA'){
	            if (tienda_sociedad === '0') {
	                mensaje("Debe escoger una tienda", 'orange');
	                $('#id_tienda').addClass('select-error');
	                return;
	               
	            }else {
	            	if(costo_gramo_base_op !== 0){
				    	costo_gramo_base_op = parseFloat(($('option:selected', '#id_tienda').attr('costo')).replace(/,/, '.'));
	            	}
				    if(precio_gramo_base_op !== 0){
				    	precio_gramo_base_op = parseFloat(($('option:selected', '#id_tienda').attr('precio')).replace(/,/, '.'));
				    }

				}
			}else{
				costo_gramo_base_op =0;
				precio_gramo_base_op =0;
			}
		}
		// cargarAdicionalesOrden();
	}else{
	
		costo_color_unitario = 0;
		tipo_transaccion = 2;
	}



	if(item_categoria === 'UNIDAD'){
		fraccion = unidades;
	}else{
		fraccion = peso;
	}

	if(externa === true){
		fraccion = unidades;
		// return false
	}

	peso = fraccion
	console.log(peso, 'peso para taller')
	// precio base
	if(origen_material === 'CLIENTE' || origen_material === 'JOYERIA'){
        costo_base_total_ta = 0;
        precio_base_total_ta = 0;
        utilidad_base_taller = 0;
        prct_utilidad_base_taller = 0;
    } else {
        precio_base_total_ta = peso * precio_gramo_base_taller;
        precio_base_total_ta = redondear(precio_base_total_ta);
        costo_base_total_ta = peso * costo_gramo_base_taller;
        costo_base_total_ta = redondear(costo_base_total_ta);
        utilidad_base_taller = precio_base_total_ta - costo_base_total_ta;
        utilidad_base_taller = redondear(utilidad_base_taller);
        if(utilidad_base_taller > 0){
            prct_utilidad_base_taller = (utilidad_base_taller/costo_base_total_ta) * 100;
            prct_utilidad_base_taller = redondear(prct_utilidad_base_taller)
        } else {
            prct_utilidad_base_taller = 0;
        }
    }

    // Precio fabricación
    console.log(costo_fabricacion_unitario, 'costo fabric unitario')
    console.log(precio_fabricacion_unitario, 'precio fabricacion unitario')
    costo_total_fabricacion_ta = peso * costo_fabricacion_unitario;
    costo_total_fabricacion_ta = redondear(costo_total_fabricacion_ta);
    precio_fabricacion_total_ta = peso * precio_fabricacion_unitario;
    console.log('*****')
    console.log(precio_fabricacion_total_ta, 'precio fabricac total taller')
    console.log(costo_total_fabricacion_ta, 'costo_frabricacion total taller')
    console.log('*****')

	precio_fabricacion_total_ta = redondear(precio_fabricacion_total_ta);
	utilidad_fabricacion_taller = precio_fabricacion_total_ta - costo_total_fabricacion_ta;
	utilidad_fabricacion_taller = redondear(utilidad_fabricacion_taller);

	if(costo_total_fabricacion_ta > 0){
            prct_util_fabricacion_taller = (utilidad_fabricacion_taller/costo_total_fabricacion_ta) * 100;
    }else{
            prct_util_fabricacion_taller = 0;
    }
    

	if(Number.isNaN(prct_util_fabricacion_taller)){
        prct_util_fabricacion_taller = 0;
    }
	console.log(prct_util_fabricacion_taller, 'prct utilidad fabric taller')
	
    // Costo color
    costo_color_total = peso * costo_color_unitario;
    costo_color_total = redondear(costo_color_total);




	subtotal_taller = precio_base_total_ta + precio_fabricacion_total_ta + total_rubros + parseFloat(precioTotalPiedrasTaller) + parseFloat(precioTotalAdicionalesTaller);
	subtotal_taller = redondear(subtotal_taller);
	console.log(subtotal_taller, 'subtotal_taller')

	costoManoObraTotal = precio_base_total_ta + precio_fabricacion_total_ta + total_rubros;
	costoManoObraTotal = redondear(costoManoObraTotal);
    impuestos_taller = subtotal_taller * (prct_impuestos_taller/100);
    impuestos_taller = redondear(impuestos_taller);

    // total taller

	total_taller = subtotal_taller + impuestos_taller;
	total_taller = redondear(total_taller);
	console.log('total taller', total_taller)
	return 


}


function cargarPiedrasOrden(){
	// buscar y agregar cliente en orden.
	cliente = localStorage.getItem('cliente') || '';
    if (cliente !== '') {
        cliente = JSON.parse(cliente);
        $('#id_cliente').val(cliente.nombres + ' ' + cliente.apellidos);
        $('#id_cliente').removeClass('is-invalid');
        $('#cliente_error').hide();
    }


}



function cargarAdicionalesOrden(){
	// Agregar Adicionales
    $('#id_adicionales').show();
    $('#id_tabla_adicionales').show();

    cliente = localStorage.getItem('cliente') || '';
    if (cliente !== '') {
        cliente = JSON.parse(cliente);
        $('#id_cliente').val(cliente.nombres + ' ' + cliente.apellidos);
        $('#id_cliente').removeClass('is-invalid');
        $('#cliente_error').hide();
    }

    adicionales_lista = localStorage.getItem('adicionales') || '';
    if (adicionales_lista === '') {
        adicionales_lista = [];
    	$('#id_adicionales').hide();
        $('#id_tabla_adicionales').hide();
    } else {
        adicionales_lista = JSON.parse(adicionales_lista);
    }

    idTabla = $('#id_adicionales_lista')

    if (idTabla) {
        $('#id_adicionales_lista').remove();
    }

    $('#id_adicionales_lista tr').remove();
    let tabla_adicional = '<table id="id_adicionales_lista" class="table table-striped table-hover"><thead><th class="all">Acciones</th><th>Descripción</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th></thead><tbody></tbody></table>';
    $('#id_tabla_adicionales').append(tabla_adicional);

    costoTotalAdicionalesTaller = 0;
    precioTotalAdicionalesTaller = 0;
    costo_adicionales = 0;
    
    variable1 =0;
    precio_totalAdiOp = 0;
    utilidadTotalAdicionales =0;
    adicionales_lista.forEach(adicional => {
    	console.log(adicional)
        cantidad = parseFloat(adicional.cantidad);
        costo_taller = parseFloat(adicional.costo);
        precio_taller = parseFloat(adicional.precio_ta);
        subtotal_adicional_taller = (cantidad * precio_taller);
        total = parseFloat(adicional.subtotal_ta)
        costoTotal = costo_taller * cantidad

        precio_adicional_op = adicional.precio_op;
        precio_totalAdiOp += parseFloat(adicional.total);

        costoTotalAdicionalesTaller += parseFloat(costoTotal);
        precioTotalAdicionalesTaller += total
        utilidadTotalAdicionales =  precio_totalAdiOp - precioTotalAdicionalesTaller;


        
        if(decimales === 'True'){
            digitos = 2;
        } else {
            digitos = 0;
        }
        if(tipo_usuario === 'USUARIO OPERACIONES'){
        	let tr = '<tr><td><button type="button" id="' + adicional.id + '" onclick="borrarAdicional(' + adicional.secuencia + ')" class="btn btn-icon rounded-circle btn-outline-danger mr-1 mb-1"><i class="bx bx-trash-alt"></i></button></td><td>' + adicional.descripcion + '</td><td style="text-align: left;">' + parseFloat(precio_adicional_op).toFixed(digitos) + '</td><td>' + adicional.cantidad + '</td><td style="text-align: left;">' + parseFloat(adicional.total).toFixed(digitos) + '</td></tr>';
        	$('#id_adicionales_lista').append(tr);
        }else{
	        let tr = '<tr><td><button type="button" id="' + adicional.id + '" onclick="borrarAdicional(' + adicional.secuencia + ')" class="btn btn-icon rounded-circle btn-outline-danger mr-1 mb-1"><i class="bx bx-trash-alt"></i></button></td><td>' + adicional.descripcion + '</td><td style="text-align: left;">' + parseFloat(precio_taller).toFixed(digitos) + '</td><td>' + adicional.cantidad + '</td><td style="text-align: left;">' + parseFloat(subtotal_adicional_taller).toFixed(digitos) + '</td></tr>';
	        $('#id_adicionales_lista').append(tr);
        }
    });
    console.log('precio total adicional storage op', precio_totalAdiOp)
    utilidadTotalAdicionales = redondear(utilidadTotalAdicionales);
    precioTotalAdicionalesTaller = redondear(precioTotalAdicionalesTaller);
    costoTotalAdicionalesTaller = redondear(costoTotalAdicionalesTaller);
    precio_totalAdiOp = redondear(precio_totalAdiOp)
    precioTotalAdicionalesOp = redondear(precio_totalAdiOp)
    
    // console.log(precioTotalAdicionalTaler, 'precio total adicionales taller')
    // console.log(costoTotalAdicionalesTaller, 'costo adicional taller')
    cantAdicionales = adicionales_lista.reduce((contadorAdicional, id) => {
            contadorAdicional[id.id] = (contadorAdicional[id.id] || 0) + 1;
            // console.log(contadorAdicional)
            return contadorAdicional;
        }, {});


    // console.log('cantidad adicionales', cantAdicionales)
    cantidadesAdicional = Object.values(cantAdicionales);
    // cantidad de adicionales
   
    for(var adicional = 0; adicional < cantidadesAdicional.length; adicional ++){
        // console.log(cantidadesAdicional)
        if(cantidadesAdicional > 1){
            mensaje('Existe al menos un adicional ingresado más de una vez', 'red');
            return false;
        }
    }
    if(adicionales_lista.length === 0){
        $('#id_adicionales_lista').remove();
    }
}


function transaccion(transacc){
	peso = parseFloat(transacc.peso)
	if(isNaN(peso)){
            peso = 0;
    }

	if((transacc.adicionales).length !== 0){
		precioTotalAdicionalesTaller = 0;
		utilidadTotalAdicionales = 0;
		precioTotalAdicionalesOp =0 ;
		transacc.adicionales.forEach(adicional => {
			
			precioTotalAdicionalesTaller +=  parseFloat(adicional.subtotal_adicional_taller);
			precioTotalAdicionalesOp += parseFloat(adicional.subtotal_adicional_operaciones);
			utilidadTotalAdicionales = parseFloat(precioTotalAdicionalesOp) - parseFloat(precioTotalAdicionalesTaller)

		})
		utilidadTotalAdicionales = redondear(utilidadTotalAdicionales);

	}else{
		cargarAdicionalesOrden();
	}

	if((transacc.piedras).length !== 0 ){
		utilidadTotalPiedrasOp = 0;
		precioTotalPiedrasTaller = 0;
		precioTotalPiedrasOp = 0;
		transacc.piedras.forEach(piedra => {
			precioTotalPiedrasTaller += parseFloat(piedra.subtotal_piedra_taller);
			precioTotalPiedrasOp += parseFloat(piedra.subtotal_piedra_operaciones);
			utilidadTotalPiedrasOp = parseFloat(piedra.subtotal_piedra_operaciones) - parseFloat(piedra.subtotal_piedra_taller);
		})
	}
	else{
		
		cargarPiedrasOrden();
	}

	origen_material_descripcion = transacc.origen

	// if (!origen_material) {
	//     mensaje("Debe escoger un origen de material", 'orange');
	//     $('#id_origen').addClass('select-error');
	//     return;
	// }
	
	peso_solicitado = peso

	if(peso_solicitado === ''){
		peso_solicitado = 0
	}else {
		peso_solicitado = peso
	}
	console.log(peso_solicitado, 'peso solicitado');
    console.log(regla_calculo_op, 'regla calculo operacion');
    console.log(regla_calculo_taller, 'regla calculo taller')
    unidades_solicitadas = transacc.unidades

    
    if(regla_calculo_op === 'NORMAL'){

    	calcularValoresTallerInversa(peso_solicitado, unidades_solicitadas, origen_material_descripcion);

    	// valores joyeria en formula normal
    	gramos_base = peso_solicitado;
    	if(item_categoria === 'UNIDAD'){
    		fraccion = unidades_solicitadas;
    	}else{
    		fraccion = peso_solicitado;
    	}
    	if(origen_material_descripcion === 'CLIENTE' || origen_material_descripcion === 'TALLER'){
    		costo_base_total_op = 0;
    		precio_base_total_op = 0;
    		utilidad_base_op = 0;
    		prct_utilidad_base_op =0;
    	}else{
    		precio_base_total_op = gramos_base * precio_gramo_base_op;
    		precio_base_total_op = redondear(precio_base_total_op);
    		costo_base_total_op = gramos_base * costo_gramo_base_op;
            costo_base_total_op = redondear(costo_base_total_op);
            utilidad_base_op = precio_base_total_op - costo_base_total_op;
            utilidad_base_op = redondear(utilidad_base_op);

            if(utilidad_base_op > 0){
            	prct_utilidad_base_op = (utilidad_base_op/costo_base_total_op) * 100;

            }else{
            	prct_utlidad_base_op = 0;
            }
    	}
    	console.log(utilidadTotalAdicionales)
    	console.log(utilidadTotalPiedrasOp)
    	console.log(prct_util_fabricacion_op, 'util fabric  prct')

    	utilidad_fabricacion_op = costoManoObraTotal * ((prct_util_fabricacion_op/100));

    	utilidad_fabricacion_op = utilidad_fabricacion_op + utilidadTotalAdicionales + utilidadTotalPiedrasOp;
    	utilidad_fabricacion_op = redondear(utilidad_fabricacion_op);
    	console.log(utilidad_fabricacion_op, 'util fabricacion op')
    	console.log(utilidad_base_op, 'utilidad base ope')

    	precio_fabricacion_total_op = subtotal_taller + utilidad_fabricacion_op;
    	precio_fabricacion_total_op = redondear(precio_fabricacion_total_op);

    	// subtotales
    	console.log(precio_fabricacion_total_op)
    	console.log(precio_base_total_op)
    	subtotal_op = precio_base_total_op + precio_fabricacion_total_op;
    	// subtotal_op = redondear(subtotal_op);

    	impuestos_op = subtotal_op * (prct_impuestos_joyeria/100);
    	impuestos_op = redondear(impuestos_op);
    	// total orden

    	total_fabricacion_op = subtotal_op + impuestos_op;
    	total_fabricacion_op = redondear(total_fabricacion_op);

    }
    // si regla de calculo de operaciones es inversa
    else{
    	calcularValoresTallerInversa(peso_solicitado, unidades_solicitadas, origen_material_descripcion);

    	if(item_categoria === 'UNIDAD'){
    		fraccion = unidades_solicitadas;
    	}else{
    		fraccion = peso_solicitado;
    	}

    	gramos_base = fraccion;
    	//  total de la orden

    	total_fabricacion_op = fraccion * precio_unitario_op;

    	total_fabricacion_op = redondear(total_fabricacion_op);
    	subtotal_op = total_fabricacion_op / (1 + (prct_impuestos_joyeria/100));
        subtotal_op = redondear(subtotal_op);
        

        impuestos_op = total_fabricacion_op - subtotal_op;
        impuestos_op = redondear(impuestos_op);

        if(origen_material_descripcion === 'CLIENTE' || origen_material_descripcion === 'TALLER'){
            costo_base_total_op = 0;
            precio_base_total_op = 0;
            utilidad_base_op = 0;
            prct_utilidad_base_op = 0;
        } else {
            precio_base_total_op = gramos_base * precio_gramo_base_op;
            precio_base_total_op = redondear(precio_base_total_op);
            
            costo_base_total_op = gramos_base * costo_gramo_base_op;
            costo_base_total_op = redondear(costo_base_total_op);
            utilidad_base_op = precio_base_total_op - costo_base_total_op;
            utilidad_base_op = redondear(utilidad_base_op);
            if(utilidad_base_op > 0){
                prct_utilidad_base_op = (utilidad_base_op/costo_base_total_op) * 100;
            } else {
                prct_utilidad_base_op = 0;
            }
        }

		utilidad_fabricacion_op = subtotal_op - costoManoObraTotal - precio_base_total_op;
		utilidad_fabricacion_op = redondear(utilidad_fabricacion_op);
		console.log(utilidad_fabricacion_op, 'utilidad fabricacion op')
		console.log(utilidad_base_op, 'utilidad base operaciones')
    	console.log(costo_base_total_op, 'costo_base_total_op')

		precio_fabricacion_total_op = subtotal_taller + utilidad_fabricacion_op;
        precio_fabricacion_total_op = redondear(precio_fabricacion_total_op);
		prct_util_fabricacion_op = ((precio_fabricacion_total_op - subtotal_taller) / subtotal_taller) * 100;
		prct_util_fabricacion_op = redondear(prct_util_fabricacion_op)

    }
    

    // calculo de valores para la orden
	if(regla_calculo_op === 'INVERSA'){
	    if(precioTotalAdicionalesOp !== 0){
	    	subtotal_transaccion = subtotal_op + parseFloat(precioTotalPiedrasOp) + parseFloat(precioTotalAdicionalesOp);
	    }else{
	    	subtotal_transaccion = subtotal_op + parseFloat(precioTotalPiedrasOp) + parseFloat(precio_totalAdiOp);
	    }
	}else{
	    subtotal_transaccion = subtotal_op;
	}

    subtotal_transaccion = redondear(subtotal_transaccion);

    // impuestos piedras y adicionales
    impuestosPiedras =  (precioTotalPiedrasOp * prct_impuestos_joyeria)/100;
    impuestosPiedras = redondear(impuestosPiedras);


    if(precioTotalAdicionalesOp !== 0){
	    	impuestosAdicional = (precioTotalAdicionalesOp * prct_impuestos_joyeria) /100;
    		impuestosAdicional = redondear(impuestosAdicional);
    }else{
    	impuestosAdicional = (precio_totalAdiOp * prct_impuestos_joyeria) /100;
    	impuestosAdicional = redondear(impuestosAdicional);
    }
    

	if(regla_calculo_op === 'INVERSA'){
	    impuestos_transaccion = impuestos_op + impuestosPiedras + impuestosAdicional ;
	}else{
	    impuestos_transaccion = subtotal_op * (prct_impuestos_joyeria/100) ;

	}
	impuestos_transaccion = redondear(impuestos_transaccion);

	precio_sistema = subtotal_transaccion + impuestos_transaccion;
	precio_sistema = redondear(precio_sistema);
	precio_final = precio_sistema;

	// if($('#id_descuento').val() !== ''){
	//     if(parseFloat($('#id_descuento').val().replace(/,/, '.')) > 0){
	//         CalcularDescuento();
	//     }
	// }

	// if($('#id_precio_negociado').val() !== ''){
	//     if(parseFloat($('#id_precio_negociado').val().replace(/,/, '.')) !== precio_final_solicitud){
	//         grabarPrecioNegociado();
	//     }
	// }


	if(decimales === 'True'){
	    precio_mostrar = precio_final.toFixed(2);
	} else {
	    precio_mostrar = Math.round(precio_final);
	}



	// agregar datos al arreglo

	transacc['peso'] = peso;
	transacc['subtotal_transaccion'] = subtotal_transaccion;
	transacc['impuestos_transaccion'] = impuestos_transaccion;


	transacc['precio_fabricacion_total_ta'] = precio_fabricacion_total_ta;
	transacc['costo_total_fabricacion_ta'] = costo_total_fabricacion_ta;
	transacc['utilidad_fabricacion_taller'] = utilidad_fabricacion_taller;
	transacc['prct_util_fabricacion_taller'] = prct_util_fabricacion_taller;

	transacc['subtotal_taller'] = subtotal_taller;
	transacc['impuestos_taller'] = impuestos_taller;
	transacc['total_taller'] = total_taller;

	transacc['subtotal_operaciones'] = subtotal_op;
	transacc['impuestos_operaciones'] = impuestos_op;
	transacc['precio_sistema'] = precio_mostrar;

	// adicionales
	transacc['precio_total_piedras_taller'] =  precioTotalPiedrasTaller;
	transacc['impuestos_piedras'] = impuestosPiedras;
	transacc['precio_total_piedras_op'] = precioTotalPiedrasOp;
	transacc['utilidad_piedras'] = utilidadTotalPiedrasOp
	// if(precioTotalAdicionalesTa !== 0){
	// 	transacc['precio_total_adicionales_taller'] = precioTotalAdicionalesTa;
	// }else{
	// }
	transacc['precio_total_adicionales_taller'] = precioTotalAdicionalesTaller;
	transacc['impuestos_adicionles'] = impuestosAdicional;
	transacc['precio_total_adicionales_op'] = precioTotalAdicionalesOp;
	transacc['utilidad_adicionales'] = redondear(utilidadTotalAdicionales, 2);

	transacc['costo_color_unitario'] = redondear(costo_color_unitario, 2)
	transacc['utilidad_fabricacion_op'] = redondear(utilidad_fabricacion_op, 2);

	// llenarDetallesCostos();
	$('#id_precio').val(simbolo_moneda + ' ' + precio_mostrar);

	console.log(peso, 'psoooooo')
	console.log(transacc)
	
	

	return transaccion

}

