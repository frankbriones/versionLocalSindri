

function calcularValoresTransaccion(itemDatos){

	let transaccionCalculada = {
		// valores taller

		'manoObraCostoUnitario': 0,
		'manoObraCostoTotal': 0,
		'manoObraUtilidadPrct': 0,
		'manoObraUtilidad': 0,
		'manoObraPrecioUnitario': 0,
		'manoObraPrecioTotal': 0,
		'servicioFabricacionTotal': 0,

		'materiaPrimaTallerCostoUnitario': 0,
		'materiaPrimaTallerCostoTotal': 0,
	    'materiaPrimaTallerUtilidadPrct': 0,
		'materiaPrimaTallerUtilidad': 0,
		'materiaPrimaTallerPrecioUnitario': 0,
		'materiaPrimaTallerPrecioTotal': 0,
		
		'rubrosCostoTotal': 0,
		'piedrasBasicasCosto': 0,
	    'colorCostoAdicionalUnitario': 0,
		'colorCostoAdicionalTotal': 0,
		
		'piedrasFinasTallerCostoTotal': 0,
		'piedrasFinasTallerPrecioTotal': 0,
		'piedrasFinasTallerUtilidad': 0,

		'adicionalesTallerCostoTotal': 0,
		'adicionalesTallerPrecioTotal': 0,
		'adicionalesTallerUtilidad': 0,

	    'subtotalTaller': 0,
	    'impuestosTallerPrct': 0,
	    'impuestosTaller': 0,
		'totalTaller': 0,

		// valores tienda

		'materiaPrimaTiendaCostoUnitario': 0,
		'materiaPrimaTiendaCostoTotal': 0,
	    'materiaPrimaTiendaUtilidadPrct': 0,
		'materiaPrimaTiendaUtilidad': 0,
		'materiaPrimaTiendaPrecioUnitario': 0,
		'materiaPrimaTiendaPrecioTotal': 0,

		'fabricacionTiendaUtilidadPrct': 0,
		'fabricacionTiendaUtilidad': 0,

		'precioFinalTiendaUnitario': 0,
		'precioFinalTiendaTotal': 0,

		'piedrasFinasTiendaCostoTotal': 0,
		'piedrasFinasTiendaPrecioTotal': 0,
		'piedrasFinasTiendaUtilidad': 0,
		'priedasFinasTiendaImpuestos': 0,

		'adicionalesTiendaCostoTotal': 0,
		'adicionalesTiendaPrecioTotal': 0,
		'adicionalesTiendaUtilidad': 0,
		'adicionalesTiendaImpuestos': 0,
		
		'subtotalTransaccion': 0,
		'impuestosTiendaPrct': 0,
		'impuestosTienda': 0,

		'precioSistema': 0,
		'descuento': 0,
		'precioFinalTransaccion': 0,

		'adicionalesLista': [],
		'piedrasFinasLista': [],

		'costoColorAdicionalTallerUnitario': 0,
        'precioColorAdicionalTallerTotal': 0,
        'precioColorAdicionalTiendaUnitario': 0,
        'precioColorAdicionalTiendaTotal': 0
	}

	// calcular valores de adicionales
	if(itemDatos.adicionalesLista.length > 0){
		itemDatos.adicionalesLista.forEach(adicional => {

			cantidad = parseFloat(adicional.cantidad);
			adicionalCostoTallerUnitario = parseFloat(adicional.costo);
			adicionalPrecioTallerUnitario = parseFloat(adicional.precio_ta);
			adicionalUtilidadTiendaPrct = parseFloat(adicional.utilidadTiendaPrct);
			adicionalCostoTallerSubtotal = cantidad * adicionalCostoTallerUnitario;
			adicionalPrecioTallerSubtotal = cantidad * adicionalPrecioTallerUnitario;
			adicionalUtilidadTallerSubtotal = adicionalPrecioTallerSubtotal - adicionalCostoTallerSubtotal;
			adicionalUtilidadTiendaSubtotal = (adicionalPrecioTallerSubtotal * (adicionalUtilidadTiendaPrct / 100));
			adicional = {
				'cantidad' : cantidad,
				'adicionalCostoTallerUnitario': adicionalCostoTallerUnitario,
				'adicionalPrecioTallerUnitario': adicionalPrecioTallerUnitario,
				'adicionalUtilidadTiendaPrct': adicionalUtilidadTiendaPrct,
				'adicionalPrecioTallerSubtotal': adicionalPrecioTallerSubtotal,
				'adicionalUtilidadTallerSubtotal': adicionalUtilidadTallerSubtotal,
				'adicionalUtilidadTiendaSubtotal': adicionalUtilidadTiendaSubtotal,
				'adicional_id': adicional.id_adicional


			}
			transaccionCalculada.adicionalesLista.push(adicional);
			transaccionCalculada.adicionalesTallerCostoTotal += adicionalCostoTallerSubtotal;
			transaccionCalculada.adicionalesTallerPrecioTotal += adicionalPrecioTallerSubtotal;
			transaccionCalculada.adicionalesTallerUtilidad += adicionalUtilidadTallerSubtotal;
			transaccionCalculada.adicionalesTiendaUtilidad += parseFloat(adicionalUtilidadTiendaSubtotal);
			transaccionCalculada.adicionalesTiendaPrecioTotal += (adicionalPrecioTallerSubtotal + parseFloat(adicionalUtilidadTiendaSubtotal));
			
			
		});
	}else{
		transaccionCalculada.adicionalesTallerCostoTotal = 0;
		transaccionCalculada.adicionalesTallerPrecioTotal =0;
		transaccionCalculada.adicionalesTallerUtilidad = 0;
		transaccionCalculada.adicionalesTiendaUtilidad = 0;
		transaccionCalculada.adicionalesTiendaPrecioTotal =0;

	}


	// calcular valores de piedras finas
	if(itemDatos.piedrasLista.length > 0){
		transaccionCalculada.piedrasFinasTallerCostoTotal = 0;
		transaccionCalculada.piedrasFinasTallerPrecioTotal = 0;
		transaccionCalculada.piedrasFinasTallerUtilidad = 0;
		transaccionCalculada.piedrasFinasTiendaUtilidad = 0;
		transaccionCalculada.piedrasFinasTiendaPrecioTotal = 0;
		
		itemDatos.piedrasLista.forEach(piedra => {
			cantidad = parseFloat(piedra.cantidad);
			piedraCostoTallerUnitario = redondear(parseFloat(piedra.costo));
			piedraPrecioTallerUnitario = redondear(parseFloat(piedra.precio_ta));
			piedraUtilidadTiendaPrct = redondear(parseFloat(piedra.utilidadTiendaPrct));

			piedraCostoTallerSubtotal = redondear(cantidad * piedraCostoTallerUnitario);
			piedraPrecioTallerSubtotal = redondear(cantidad * piedraPrecioTallerUnitario);
			piedraUtilidadTallerSubtotal = redondear(piedraPrecioTallerSubtotal - piedraCostoTallerSubtotal);
			piedraUtilidadTiendaSubtotal = redondear(parseFloat(piedraPrecioTallerSubtotal * (piedraUtilidadTiendaPrct / 100)));

			piedras = {
				'cantidad' : cantidad,
				'piedraCostoTallerUnitario': piedraCostoTallerUnitario,
				'piedraPrecioTallerUnitario': piedraPrecioTallerUnitario,
				'piedraUtilidadTiendaPrct': piedraUtilidadTiendaPrct,
				'piedraPrecioTallerSubtotal': piedraPrecioTallerSubtotal,
				'piedraUtilidadTallerSubtotal': piedraUtilidadTallerSubtotal,
				'piedraUtilidadTiendaSubtotal': piedraUtilidadTiendaSubtotal,
				'piedra_id': piedra.id_piedra


			}
			transaccionCalculada.piedrasFinasLista.push(piedras)


			transaccionCalculada.piedrasFinasTallerCostoTotal += redondear(piedraCostoTallerSubtotal);
			transaccionCalculada.piedrasFinasTallerPrecioTotal += redondear( piedraPrecioTallerSubtotal);
			transaccionCalculada.piedrasFinasTallerUtilidad += redondear(piedraUtilidadTallerSubtotal);
			transaccionCalculada.piedrasFinasTiendaUtilidad += redondear(piedraUtilidadTiendaSubtotal);
			transaccionCalculada.piedrasFinasTiendaPrecioTotal += redondear((piedraPrecioTallerSubtotal + piedraUtilidadTiendaSubtotal));
		});
	}else{
		transaccionCalculada.piedrasFinasTallerCostoTotal = 0;
		transaccionCalculada.piedrasFinasTallerPrecioTotal = 0;
		transaccionCalculada.piedrasFinasTallerUtilidad = 0;
		transaccionCalculada.piedrasFinasTiendaUtilidad = 0;
		transaccionCalculada.piedrasFinasTiendaPrecioTotal = 0;

	}

	// calcular costos de materia prima
	if(itemDatos.materiaPrimaOrigen === 'TALLER'){
		
		transaccionCalculada.materiaPrimaTallerCostoTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTallerCostoUnitario);
		transaccionCalculada.materiaPrimaTallerPrecioTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTallerPrecioUnitario);
		transaccionCalculada.materiaPrimaTallerUtilidad = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal - transaccionCalculada.materiaPrimaTallerCostoTotal);
		if(transaccionCalculada.materiaPrimaTallerUtilidad > 0){
            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear((transaccionCalculada.materiaPrimaTallerUtilidad / transaccionCalculada.materiaPrimaTallerCostoTotal) * 100);
            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTallerUtilidadPrct);
        } else {
            transaccionCalculada.materiaPrimaTallerUtilidadPrct = 0;
		}

	}

	if(itemDatos.materiaPrimaOrigen === 'JOYERIA'){
		transaccionCalculada.materiaPrimaTiendaCostoTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaCostoUnitario);
		transaccionCalculada.materiaPrimaTiendaPrecioTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaPrecioUnitario);
		if(itemDatos.fabricacionInterna === true){
			transaccionCalculada.materiaPrimaTiendaUtilidad = 0;
			transaccionCalculada.materiaPrimaTiendaUtilidadPrct = 0;
		}else {
			transaccionCalculada.materiaPrimaTiendaUtilidad = redondear(transaccionCalculada.materiaPrimaTiendaPrecioTotal - transaccionCalculada.materiaPrimaTiendaCostoTotal);
			if(transaccionCalculada.materiaPrimaTiendaUtilidad > 0 ){
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidad / transaccionCalculada.materiaPrimaTiendaCostoTotal) * 100;
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidadPrct);
			} 
		}

		
	}


	if(itemDatos.materiaPrimaOrigen === 'CLIENTE'){

		if(itemDatos.fabricacionDividida === 1 ){
			// valores del taller
			transaccionCalculada.materiaPrimaTallerCostoTotal = redondear(itemDatos.pesoSolicitado * itemDatos.materiaPrimaTallerCostoUnitario);
			transaccionCalculada.materiaPrimaTallerPrecioTotal = redondear(itemDatos.pesoSolicitado * itemDatos.materiaPrimaTallerPrecioUnitario);

			transaccionCalculada.materiaPrimaTallerUtilidad = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal - transaccionCalculada.materiaPrimaTallerCostoTotal);
			if(transaccionCalculada.materiaPrimaTallerUtilidad > 0){
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear((transaccionCalculada.materiaPrimaTallerUtilidad / transaccionCalculada.materiaPrimaTallerCostoTotal) * 100);
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTallerUtilidadPrct);
	        } else {
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = 0;
			}

			
			// valores de la joyeria
			transaccionCalculada.materiaPrimaTiendaCostoTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaCostoUnitario);

			transaccionCalculada.materiaPrimaTiendaPrecioTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaPrecioUnitario);
			transaccionCalculada.materiaPrimaTiendaUtilidad = redondear(redondear(itemDatos.pesoSolicitado * itemDatos.materiaPrimaTiendaPrecioUnitario) - redondear(itemDatos.pesoSolicitado * itemDatos.materiaPrimaTiendaCostoUnitario));
			
			if(transaccionCalculada.materiaPrimaTiendaUtilidad > 0){
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidad / transaccionCalculada.materiaPrimaTiendaCostoTotal) * 100;
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidadPrct);
			} else {
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = 0;
			}

		// en caso de no ser una fabricacion dividida con el cliente.
		}else{
			transaccionCalculada.materiaPrimaTallerCostoTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTallerCostoUnitario);
			transaccionCalculada.materiaPrimaTallerPrecioTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTallerPrecioUnitario);
			transaccionCalculada.materiaPrimaTallerUtilidad = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal - transaccionCalculada.materiaPrimaTallerCostoTotal);
			if(transaccionCalculada.materiaPrimaTallerUtilidad > 0){
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear((transaccionCalculada.materiaPrimaTallerUtilidad / transaccionCalculada.materiaPrimaTallerCostoTotal) * 100);
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTallerUtilidadPrct);
	        } else {
	            transaccionCalculada.materiaPrimaTallerUtilidadPrct = 0;
			}

			
			// valores de la joyeria
			transaccionCalculada.materiaPrimaTiendaCostoTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaCostoUnitario);

			transaccionCalculada.materiaPrimaTiendaPrecioTotal = redondear(itemDatos.gramos * itemDatos.materiaPrimaTiendaPrecioUnitario);
			transaccionCalculada.materiaPrimaTiendaUtilidad = redondear(transaccionCalculada.materiaPrimaTiendaPrecioTotal - transaccionCalculada.materiaPrimaTiendaCostoTotal);
			if(transaccionCalculada.materiaPrimaTiendaUtilidad > 0){
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidad / transaccionCalculada.materiaPrimaTiendaCostoTotal) * 100;
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = redondear(transaccionCalculada.materiaPrimaTiendaUtilidadPrct);
			} else {
				transaccionCalculada.materiaPrimaTiendaUtilidadPrct = 0;
			}
		}
	}

	// calcular valores de taller
	if(itemDatos.tallerPrecioTipo === 'UNIDAD'){
		

		transaccionCalculada.manoObraCostoTotal = redondear(itemDatos.unidades * itemDatos.manoObraCostoUnitario);
		transaccionCalculada.manoObraPrecioTotal = redondear(itemDatos.unidades * itemDatos.manoObraPrecioUnitario) ;
		transaccionCalculada.manoObraUtilidad = redondear(transaccionCalculada.manoObraPrecioTotal - transaccionCalculada.manoObraCostoTotal);
		
		transaccionCalculada.subtotalTaller = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal + transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.adicionalesTallerPrecioTotal + transaccionCalculada.piedrasFinasTallerPrecioTotal + itemDatos.rubrosCostoTotal);
		transaccionCalculada.impuestosTaller = redondear(transaccionCalculada.subtotalTaller * (itemDatos.impuestosTallerPrct / 100));
		transaccionCalculada.totalTaller = redondear(transaccionCalculada.subtotalTaller + transaccionCalculada.impuestosTaller);
		transaccionCalculada.impuestosTallerPrct = redondear(itemDatos.impuestosTallerPrct);
		transaccionCalculada.rubrosCostoTotal = redondear(itemDatos.rubrosCostoTotal);

		transaccionCalculada.precioColorAdicionalTallerUnitario = redondear(itemDatos.precioColorAdicionalTallerUnitario);
		transaccionCalculada.precioColorAdicionalTallerTotal = redondear(itemDatos.gramos * transaccionCalculada.precioColorAdicionalTallerUnitario);
		transaccionCalculada.servicioFabricacionTotal = redondear(transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.colorCostoAdicionalTotal  + itemDatos.rubrosCostoTotal + itemDatos.piedrasBasicasCosto);


	}

	if(itemDatos.tallerPrecioTipo === 'GRAMO_FINAL_VARIABLE'){
		// itemDatos.gramos= itemDatos.pesoSolicitado

		// transaccionCalculada.manoObraCostoTotal = (itemDatos.unidades * itemDatos.manoObraCostoUnitario) ;
		// transaccionCalculada.manoObraUtilidad = transaccionCalculada.manoObraPrecioTotal * (transaccionCalculada.manoObraUtilidadPrct / 100);
		// transaccionCalculada.manoObraPrecioTotal = transaccionCalculada.manoObraCostoTotal + transaccionCalculada.manoObraUtilidad;
		transaccionCalculada.manoObraUtilidadPrct = redondear(itemDatos.manoObraUtilidadPrct);
		transaccionCalculada.manoObraCostoTotal = redondear(itemDatos.gramos * itemDatos.manoObraCostoUnitario) ;
		transaccionCalculada.manoObraPrecioTotal = redondear(itemDatos.gramos * itemDatos.manoObraPrecioUnitario);
		// console.log(transaccionCalculada.manoObraPrecioUnitario)
		// console.log(transaccionCalculada.manoObraPrecioTotal)
		transaccionCalculada.manoObraUtilidad = redondear(transaccionCalculada.manoObraPrecioTotal * (transaccionCalculada.manoObraUtilidadPrct / 100));

		transaccionCalculada.rubrosCostoTotal = redondear(itemDatos.rubrosCostoTotal);

		transaccionCalculada.precioColorAdicionalTallerUnitario = redondear(itemDatos.precioColorAdicionalTallerUnitario);
		transaccionCalculada.precioColorAdicionalTallerTotal = redondear(itemDatos.gramos * transaccionCalculada.precioColorAdicionalTallerUnitario);
		// transaccionCalculada.materiaPrimaTallerPrecioUnitario = itemDatos.materiaPrimaTallerPrecioUnitario
		// transaccionCalculada.materiaPrimaTallerPrecioTotal = transaccionCalculada.materiaPrimaTallerPrecioUnitario * itemDatos.gramos
		if(itemDatos.costoEnvio === undefined){
			itemDatos.costoEnvio = 0
		}

		transaccionCalculada.servicioFabricacionTotal = redondear(transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.colorCostoAdicionalTotal  + itemDatos.rubrosCostoTotal + itemDatos.piedrasBasicasCosto);
		transaccionCalculada.subtotalTaller = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal + transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.adicionalesTallerPrecioTotal + transaccionCalculada.piedrasFinasTallerPrecioTotal + itemDatos.rubrosCostoTotal + parseFloat(itemDatos.costoEnvio));
		transaccionCalculada.impuestosTaller = redondear(transaccionCalculada.subtotalTaller * (itemDatos.impuestosTallerPrct / 100));
		transaccionCalculada.totalTaller = redondear(transaccionCalculada.subtotalTaller + transaccionCalculada.impuestosTaller);
		transaccionCalculada.impuestosTallerPrct = redondear(itemDatos.impuestosTallerPrct);

	}

	if(itemDatos.tallerPrecioTipo === 'GRAMO_FINAL_FIJO'){
		if(itemDatos.fabricacionDividida === 0 ){
			transaccionCalculada.piedrasBasicasCosto = itemDatos.piedrasBasicasCosto

			transaccionCalculada.precioColorAdicionalTallerUnitario = parseFloat(itemDatos.precioColorAdicionalTallerUnitario);
			transaccionCalculada.precioColorAdicionalTiendaTotal = redondear(parseFloat(itemDatos.gramos) * parseFloat(itemDatos.precioColorAdicionalTallerUnitario))


			transaccionCalculada.manoObraCostoUnitario = itemDatos.manoObraCostoUnitario;
			transaccionCalculada.manoObraCostoTotal = redondear(itemDatos.gramos * itemDatos.manoObraCostoUnitario);
			transaccionCalculada.manoObraPrecioTotal = redondear(itemDatos.gramos * itemDatos.manoObraPrecioUnitario);
			transaccionCalculada.manoObraUtilidad = redondear(transaccionCalculada.manoObraPrecioTotal - transaccionCalculada.manoObraCostoTotal);
			
			transaccionCalculada.rubrosCostoTotal = redondear(itemDatos.rubrosCostoTotal);

			transaccionCalculada.precioColorAdicionalTallerUnitario = redondear(itemDatos.precioColorAdicionalTallerUnitario);
			transaccionCalculada.precioColorAdicionalTallerTotal = redondear(itemDatos.gramos * transaccionCalculada.precioColorAdicionalTallerUnitario);
			transaccionCalculada.servicioFabricacionTotal = redondear(transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.precioColorAdicionalTiendaTotal  + itemDatos.rubrosCostoTotal + itemDatos.piedrasBasicasCosto);
			// console.log(transaccionCalculada.manoObraPrecioTotal, 'mano de obra total');
			// console.log(transaccionCalculada.precioColorAdicionalTiendaTotal, 'precio total de color');

			// console.log(transaccionCalculada.servicioFabricacionTotal)
			transaccionCalculada.subtotalTaller = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal +  transaccionCalculada.adicionalesTallerPrecioTotal + transaccionCalculada.piedrasFinasTallerPrecioTotal + transaccionCalculada.servicioFabricacionTotal );
			// console.log(transaccionCalculada.subtotalTaller);
			transaccionCalculada.impuestosTaller = redondear(transaccionCalculada.subtotalTaller * (itemDatos.impuestosTallerPrct / 100));
			transaccionCalculada.totalTaller = redondear(transaccionCalculada.subtotalTaller + transaccionCalculada.impuestosTaller);
			transaccionCalculada.impuestosTallerPrct = redondear(itemDatos.impuestosTallerPrct);
		}else{

			transaccionCalculada.piedrasBasicasCosto = itemDatos.piedrasBasicasCosto

			transaccionCalculada.precioColorAdicionalTallerUnitario = parseFloat(itemDatos.precioColorAdicionalTallerUnitario);
			transaccionCalculada.precioColorAdicionalTiendaTotal = redondear(parseFloat(itemDatos.pesoSolicitado) * parseFloat(itemDatos.precioColorAdicionalTallerUnitario))


			transaccionCalculada.manoObraCostoUnitario = itemDatos.manoObraCostoUnitario;
			transaccionCalculada.manoObraCostoTotal = redondear(itemDatos.pesoSolicitado * itemDatos.manoObraCostoUnitario);
			transaccionCalculada.manoObraPrecioTotal = redondear(itemDatos.pesoSolicitado * itemDatos.manoObraPrecioUnitario);
			transaccionCalculada.manoObraUtilidad = redondear(transaccionCalculada.manoObraPrecioTotal - transaccionCalculada.manoObraCostoTotal);
			
			transaccionCalculada.rubrosCostoTotal = redondear(itemDatos.rubrosCostoTotal);

			transaccionCalculada.precioColorAdicionalTallerUnitario = redondear(itemDatos.precioColorAdicionalTallerUnitario);
			transaccionCalculada.precioColorAdicionalTallerTotal = redondear(itemDatos.pesoSolicitado * transaccionCalculada.precioColorAdicionalTallerUnitario);
			transaccionCalculada.servicioFabricacionTotal = redondear(transaccionCalculada.manoObraPrecioTotal + transaccionCalculada.precioColorAdicionalTiendaTotal  + itemDatos.rubrosCostoTotal + itemDatos.piedrasBasicasCosto);
			// console.log(transaccionCalculada.manoObraPrecioTotal, 'mano de obra total');
			// console.log(transaccionCalculada.precioColorAdicionalTiendaTotal, 'precio total de color');

			// console.log(transaccionCalculada.servicioFabricacionTotal)
			transaccionCalculada.subtotalTaller = redondear(transaccionCalculada.materiaPrimaTallerPrecioTotal +  transaccionCalculada.adicionalesTallerPrecioTotal + transaccionCalculada.piedrasFinasTallerPrecioTotal + transaccionCalculada.servicioFabricacionTotal );
			// console.log(transaccionCalculada.subtotalTaller);
			transaccionCalculada.impuestosTaller = redondear(transaccionCalculada.subtotalTaller * (itemDatos.impuestosTallerPrct / 100));
			transaccionCalculada.totalTaller = redondear(transaccionCalculada.subtotalTaller + transaccionCalculada.impuestosTaller);
			transaccionCalculada.impuestosTallerPrct = redondear(itemDatos.impuestosTallerPrct);

		}


		




	}


	// calcular valores de tienda
	if(itemDatos.tiendaPrecioTipo === 'UNIDAD'){

		transaccionCalculada.precioColorAdicionalTiendaTotal = redondear(itemDatos.gramos * itemDatos.precioColorAdicionalTiendaUnitario)
		transaccionCalculada.precioColorAdicionalTiendaUnitario = itemDatos.precioColorAdicionalTiendaUnitario;

		transaccionCalculada.precioFinalTiendaTotal = redondear(itemDatos.unidades * itemDatos.precioFinalTiendaUnitario);
		transaccionCalculada.priedasFinasTiendaImpuestos = redondear(transaccionCalculada.piedrasFinasTiendaPrecioTotal * (itemDatos.impuestosTiendaPrct / 100));
		transaccionCalculada.adicionalesTiendaImpuestos = redondear(transaccionCalculada.adicionalesTiendaPrecioTotal * (itemDatos.impuestosTiendaPrct / 100));
		transaccionCalculada.precioFinalTiendaUnitario = redondear(itemDatos.precioFinalTiendaUnitario);

		transaccionCalculada.precioSistema = redondear(transaccionCalculada.precioFinalTiendaTotal + transaccionCalculada.piedrasFinasTiendaPrecioTotal + transaccionCalculada.priedasFinasTiendaImpuestos + transaccionCalculada.adicionalesTiendaPrecioTotal + transaccionCalculada.adicionalesTiendaImpuestos + transaccionCalculada.precioColorAdicionalTiendaTotal);

		if(itemDatos.precioNegociado === 0){
			transaccionCalculada.precioFinalTransaccion = redondear(transaccionCalculada.precioSistema);
		} else {
			transaccionCalculada.precioFinalTransaccion = redondear(itemDatos.precioNegociado);
			transaccionCalculada.descuento = itemDatos.descuento;
		}

		transaccionCalculada.subtotalTransaccion = redondear(transaccionCalculada.precioFinalTransaccion / (1 + (itemDatos.impuestosTiendaPrct / 100)));
		transaccionCalculada.impuestosTienda = redondear(transaccionCalculada.precioFinalTransaccion - transaccionCalculada.subtotalTransaccion);

		transaccionCalculada.fabricacionTiendaUtilidad = redondear(transaccionCalculada.subtotalTransaccion - transaccionCalculada.piedrasFinasTiendaUtilidad - transaccionCalculada.adicionalesTiendaUtilidad - transaccionCalculada.materiaPrimaTiendaPrecioTotal - transaccionCalculada.subtotalTaller);
		transaccionCalculada.impuestosTiendaPrct = redondear(itemDatos.impuestosTiendaPrct);
	}

	if(itemDatos.tiendaPrecioTipo === 'GRAMO_FINAL_VARIABLE'){

		transaccionCalculada.fabricacionTiendaUtilidadPrct = redondear(itemDatos.fabricacionTiendaUtilidadPrct);
		transaccionCalculada.fabricacionTiendaUtilidad = redondear(transaccionCalculada.servicioFabricacionTotal * (itemDatos.fabricacionTiendaUtilidadPrct / 100));
		transaccionCalculada.precioFinalTiendaTotal = redondear(transaccionCalculada.subtotalTaller + transaccionCalculada.materiaPrimaTiendaPrecioTotal + transaccionCalculada.fabricacionTiendaUtilidad);
		transaccionCalculada.subtotalTransaccion = redondear(transaccionCalculada.precioFinalTiendaTotal + transaccionCalculada.piedrasFinasTiendaUtilidad + transaccionCalculada.adicionalesTiendaUtilidad);
		transaccionCalculada.precioFinalTiendaUnitario = redondear(itemDatos.precioFinalTiendaUnitario);

		transaccionCalculada.impuestosTienda = redondear(transaccionCalculada.subtotalTransaccion * (itemDatos.impuestosTiendaPrct / 100));
		transaccionCalculada.precioSistema = redondear(transaccionCalculada.subtotalTransaccion + transaccionCalculada.impuestosTienda);
		transaccionCalculada.impuestosTiendaPrct = redondear(itemDatos.impuestosTiendaPrct);

		if(itemDatos.precioNegociado === 0){
			transaccionCalculada.precioFinalTransaccion = redondear(transaccionCalculada.precioSistema);
		} else {
			transaccionCalculada.precioFinalTransaccion = redondear(itemDatos.precioNegociado);
			transaccionCalculada.descuento = itemDatos.descuento;

			transaccionCalculada.subtotalTransaccion = redondear(transaccionCalculada.precioFinalTransaccion / (1 + (itemDatos.impuestosTiendaPrct / 100)));

			transaccionCalculada.impuestosTienda = redondear(transaccionCalculada.precioFinalTransaccion - transaccionCalculada.subtotalTransaccion);
			transaccionCalculada.fabricacionTiendaUtilidad = redondear(transaccionCalculada.subtotalTransaccion - transaccionCalculada.piedrasFinasTiendaUtilidad - transaccionCalculada.adicionalesTiendaUtilidad - transaccionCalculada.materiaPrimaTiendaPrecioTotal - transaccionCalculada.subtotalTaller);
		}

	}

	if(itemDatos.tiendaPrecioTipo === 'GRAMO_FINAL_FIJO'){
		if(itemDatos.fabricacionDividida === 0 ){
			itemDatos.gramos = itemDatos.pesoSolicitado;
			
		}

		// transaccionCalculada.precioColorAdicionalTiendaUnitario = parseFloat(itemDatos.precioColorAdicionalTallerUnitario);
		// transaccionCalculada.precioColorAdicionalTiendaTotal = redondear(parseFloat(itemDatos.gramos) * parseFloat(itemDatos.precioColorAdicionalTiendarUnitario))


		transaccionCalculada.materiaPrimaTiendaCostoUnitario = parseFloat(itemDatos.materiaPrimaTiendaCostoUnitario);
		transaccionCalculada.materiaPrimaTiendaPrecioUnitario = parseFloat(itemDatos.materiaPrimaTiendaPrecioUnitario);
		transaccionCalculada.materiaPrimaTiendaPrecioTotal = redondear(itemDatos.gramos * parseFloat(transaccionCalculada.materiaPrimaTiendaPrecioUnitario));
		transaccionCalculada.materiaPrimaTiendaCostoTotal = redondear(itemDatos.gramos * parseFloat(transaccionCalculada.materiaPrimaTiendaCostoUnitario));


		transaccionCalculada.precioColorAdicionalTiendaUnitario = parseFloat(itemDatos.precioColorAdicionalTiendaUnitario);
		transaccionCalculada.precioColorAdicionalTiendaTotal = redondear(itemDatos.gramos * parseFloat(itemDatos.precioColorAdicionalTiendaUnitario))
		
		transaccionCalculada.precioFinalTiendaTotal = redondear(itemDatos.gramos * itemDatos.precioFinalTiendaUnitario);
		transaccionCalculada.priedasFinasTiendaImpuestos = redondear(transaccionCalculada.piedrasFinasTiendaPrecioTotal * (itemDatos.impuestosTiendaPrct / 100));
		transaccionCalculada.adicionalesTiendaImpuestos = redondear(transaccionCalculada.adicionalesTiendaPrecioTotal * (itemDatos.impuestosTiendaPrct / 100));
		transaccionCalculada.precioFinalTiendaUnitario = redondear(itemDatos.precioFinalTiendaUnitario);
		transaccionCalculada.precioSistema = redondear(transaccionCalculada.precioFinalTiendaTotal + transaccionCalculada.piedrasFinasTiendaPrecioTotal + transaccionCalculada.priedasFinasTiendaImpuestos + transaccionCalculada.adicionalesTiendaPrecioTotal + transaccionCalculada.adicionalesTiendaImpuestos + transaccionCalculada.precioColorAdicionalTiendaTotal);
		if(itemDatos.precioNegociado === 0){
			transaccionCalculada.precioFinalTransaccion = redondear(transaccionCalculada.precioSistema);
		} else {
			transaccionCalculada.precioFinalTransaccion = redondear(itemDatos.precioNegociado);
			transaccionCalculada.descuento = itemDatos.descuento;
		}

		transaccionCalculada.subtotalTransaccion = redondear(transaccionCalculada.precioFinalTransaccion / (1 + (itemDatos.impuestosTiendaPrct / 100)));
		// console.log('/valores de fabricacion tienda utilidad')
		// console.log(transaccionCalculada.subtotalTransaccion);
		// console.log(transaccionCalculada.piedrasFinasTiendaUtilidad);
		// console.log(transaccionCalculada.adicionalesTiendaUtilidad);
		// console.log(transaccionCalculada.materiaPrimaTiendaPrecioTotal)
		// console.log(transaccionCalculada.subtotalTaller)


		transaccionCalculada.impuestosTienda = redondear(transaccionCalculada.precioFinalTransaccion - transaccionCalculada.subtotalTransaccion);
		transaccionCalculada.fabricacionTiendaUtilidad = redondear(transaccionCalculada.subtotalTransaccion - transaccionCalculada.piedrasFinasTiendaUtilidad - transaccionCalculada.adicionalesTiendaUtilidad - transaccionCalculada.materiaPrimaTiendaPrecioTotal - transaccionCalculada.subtotalTaller);
		transaccionCalculada.impuestosTiendaPrct = redondear(itemDatos.impuestosTiendaPrct);

	}

	console.log(itemDatos)
	console.log(transaccionCalculada);
	return transaccionCalculada

}


function redondear(valor){
        if(itemDatos.decimales === 'True'){
            return Math.round(valor * 100) / 100;
        } else {
            return Math.round(valor);
        }
    }
