-- ultima utilización 2020-01-13

INSERT INTO bases_estados(id_estado, descripcion)
VALUES(1,'ACTIVO'),
(11,'CANCELADA OP'),
(18,'CANCELADO'),
(8,'COTIZADO TALLER'),
(14,'EN PROCESO'),
(3,'ESPERA COTIZACION TALLER'),
(4,'ESPERA DE EVALUACION'),
(19,'FINALIZADO'),
(7,'GENERADO CON EXTERNO'),
(10,'GENERADO CON TALLER'),
(2,'INACTIVO'),
(12,'INGRESADO'),
(13,'MATERIAL ENVIADO'),
(16,'PRODUCTO ENVIADO'),
(17,'PRODUCTO RECIBIDO'),
(9,'RECHAZADO CLIENTE'),
(5,'RECHAZADO TALLER'),
(6,'SOLICITADO A EXTERNO'),
(15,'TRABAJO TERMINADO'),
(20,'PENDIENTE INICIO'),
(21,'CREADA'),
(22,'CONFIRMADA'),
(23,'PAGADA');


-- regiones
INSERT INTO ubc_regiones(fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_region, nombre, estado_id)
VALUES 
(curdate(), 1, curdate(), 1, 1, 'NEUTRO', 1),
(curdate(), 1, curdate(), NULL, 2, 'AMÉRICA LATINA', 1);


-- paises
INSERT INTO ubc_paises (fecha_creacion, 
			usuario_crea, 
			fecha_modificacion, 
			usuario_modifica, 
			id_pais, 
			nombre, 
			iniciales, 
			aut_externo, 
			bandera, 
			estado_id, 
			region_id, 
			zona_horaria, 
			decimales, 
			simbolo_moneda) 
VALUES
(CURDATE(), 1, CURDATE(), 1, 1, 'NEUTRO', 'NN', 1, '/banderas/latam.png', 1, 1, 'ZONA_HORARIO_DESERT', 0, 'D'),
(CURDATE(), 1, CURDATE(), 1, 2, 'COLOMBIA', 'CO', 1, 'banderas/co.png', 1, 2, 'ZONA_HORARIO_DESERT', 0, 'D'),
(CURDATE(), 1, CURDATE(), 1, 3, 'CHILE', 'CL', 1, 'banderas/cl.png', 1, 2, 'ZONA_HORARIO_DESERT', 0, 'D'),
(CURDATE(), 1, CURDATE(), 1, 4, 'BRASIL', 'BR', 1, 'banderas/br.png', 1, 2, 'ZONA_HORARIO_DESERT', 0, 'D'),
(CURDATE(), 1, CURDATE(), 1, 5, 'PERU', 'PE', 1, 'banderas/pe.png', 1, 2, 'ZONA_HORARIO_DESERT', 0, 'D'),
(CURDATE(), 1, CURDATE(), 1, 6, 'ECUADOR', 'EC', 1, 'banderas/ec.png', 1, 2, 'ZONA_HORARIO_DESERT', 0, 'D');



-- localidades
INSERT INTO ubc_localidades (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_localidad, nombre, estado_id, pais_id) 
VALUES
(curdate(), 1, curdate(), 1, 1, 'NEUTRO', 1, 1),
(curdate(), 1, curdate(), 1, 2, 'GUAYAS', 1, 6);



-- ciudades
INSERT INTO ubc_ciudades (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_ciudad, nombre, estado_id, localidad_id, pais_id)
VALUES
 (curdate(), 1, curdate(), 1, 1, 'NEUTRO', 1, 1, 1),
 (curdate(), 1, curdate(), 1, 2, 'GUAYAQUIL', 1, 2, 6);



-- zonas
INSERT INTO ubc_zonas (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_zona, nombre, estado_id, pais_id) 
VALUES 
(curdate(), 1, curdate(), 1, 1, 'NEUTRO', 1, 1),
(curdate(), 1, curdate(), 1, 2, 'ZONA GENERAL EC', 1, 6);



-- sectores
INSERT INTO ubc_sectores (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_sector, nombre, estado_id, zona_id, pais_id) 
VALUES 
(curdate(), 1, curdate(), 1, 1, 'NEUTRO', 1, 1, 1),
(curdate(), 1, curdate(), 1, 2, 'SECTOR GENERAL EC', 1, 2, 6);



-- tipo usuarios
INSERT INTO usr_tipousuarios (id_tipo_usuario, tipo_usuario, descripcion) 
VALUES 
(1,'ADMINISTRADOR','ADMINISTRADOR'),
(2,'TALLER','USUARIO TALLER'),
(3,'OPERACIONES','USUARIO OPERACIONES');


-- grupos
INSERT INTO auth_group (id, name) 
VALUES 
(1,'ADMINISTRADOR'),(3,'NN_ADMINISTRADOR_ADMIN OPERACIONES'),
(2,'NN_ADMINISTRADOR_ADMIN TALLER');



-- configuracion general
INSERT INTO cfg_configgeneral (id, 
								fecha_creacion, 
								usuario_crea, 
								fecha_modificacion, 
								usuario_modifica, 
								utilidad_sobre_base,
								limite_venta,
								aut_externo,
								descuento_max,
								pais_id,
								costo_gramo_base,
								empresa,
								utilidad_sobre_taller,
								configurado,
								origen_material) 
VALUES 
(1, curdate(), 1, curdate(), 1, 0, 10, 0, 10, 1, 20, 'NEUTRO', 5, 0, 1);



-- creacion de estandares de talla

insert into ctg_estandartallas(fecha_creacion, usuario_crea, id_estandar, descripcion, fecha_modificacion)
values (now(), 1, 1, 'Talla Americana', now());
insert into ctg_estandartallas(fecha_creacion, usuario_crea, id_estandar, descripcion, fecha_modificacion)
values (now(), 1, 2, 'Talla Europea', now());



-- taller
INSERT INTO est_talleres (fecha_creacion, 
						usuario_crea, 
						fecha_modificacion, 
						usuario_modifica,
						id_taller,
						nombre,
						costo_gramo_fabricacion,
						precio_gramo_fabricacion,
						costo_gramo_base,
						precio_gramo_base,
						utilidad_sobre_fabricacion,
						utilidad_sobre_base,
						utilidad_sobre_piedras,
						utilidad_sobre_adicionales,
						prct_impuestos,
						tmp_resp_sol,
						escala_peso,
						estandar_tallas,
						configurado,
						externo,
						secuencia_ordenes,
						secuencia_solicitudes,
						prioridad,
						logotipo,
						recalcular_precio,
						cargar_img_fin_trabajo,
						tipo_precio_predefinido,
						estado_id,
						pais_id) 
VALUES 
(curdate(), 1, curdate(), 1, 'NEUTRO', 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0, 0,1,1);



-- roles
INSERT INTO usr_roles (fecha_creacion, 
						usuario_crea, 
						fecha_modificacion, 
						usuario_modifica, 
						id_rol, 
						descripcion,
						primario,
						admin, 
						zonal,
						tipo_usuario_id, 
						grupo_id, 
						estado_id) 
VALUES 
(CURDATE(), 1, CURDATE(), 1, 1, 'ADMINISTRADOR', 1, 1, 0, 1, 1, 1),
(CURDATE(), 1, CURDATE(), 1, 2, 'ADMIN TALLER', 1, 2, 0, 2, 1, 1),
(CURDATE(), 1, CURDATE(), 1, 3, 'ADMIN OPERACIONES', 1, 3, 0, 3, 1, 1);



-- tipo catalogo
INSERT INTO ctg_tiposcatalogo (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_tipo_catalogo, descripcion, estado_id)
VALUES 
(curdate(), 1, curdate(), 1, 1, 'PRODUCTOS', 1),
(curdate(), 1, curdate(), 1, 2, 'SERVICIOS', 1);


-- Reglas para calcular precios
INSERT INTO ctg_reglascalcularprecio (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_regla, descripcion, estado_id) 
VALUES
(curdate(), 1, curdate(), 1, 1, 'NORMAL', 1),
(curdate(), 1, curdate(), 1, 2, 'INVERSA', 1);


-- Tipos de precios
INSERT INTO ctg_tiposprecios (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, id_tipo, descripcion, estado_id, regla_calculo_id)
VALUES
(curdate(), 1, curdate(), 1, 1, 'GRAMO_FINAL_FIJO', 1, 2),
(curdate(), 1, curdate(), 1, 2, 'UNIDAD', 1, 2),
(curdate(), 1, curdate(), 1, 3, 'GRAMO_FINAL_VARIABLE', 1, 1);


-- Crear colores
insert into ctg_colores (fecha_creacion, 
							usuario_crea, 
							fecha_modificacion, 
							usuario_modifica, 
							id_color, 
							descripcion, 
							estado_id, 
							pais_id, 
							taller_id,
							costo_adicional)
values(now(), 1, now(), 1, 3, 'SIN COLOR', 1, 1, 1, 0);



-- Origen material
insert into trn_origenmaterial VALUES(curdate(), 1, curdate(), 2, 1,'JOYERIA' );
insert into trn_origenmaterial VALUES(curdate(), 1, curdate(), 2, 2,'TALLER' );
insert into trn_origenmaterial VALUES(curdate(), 1, curdate(), 2, 3,'CLIENTE' );



-- Proveedores
insert into prv_proveedores (id,
								fecha_creacion,
								usuario_crea,
								fecha_modificacion,
								usuario_modifica,
								identificacion,
								nombres,
								apellidos,
								direccion,
								telefono,
								correo,
								tipo_usuario,
								taller,
								ciudad_id,
								estado_id,
								pais_id,
								zona_id) 
VALUES(1, CURDATE(), 1, CURDATE(), 1, '0994466349', 'Julio Alberto', 'Moran', 'Elizalde 119 y Pichincha', '0994466349', 'jmoran@orocash.ec', 1, 1, 1, 1, 1, 1);



insert into ctg_unidadesmedida 
values 
(curdate(), 1, CURDATE(), 1, 1, 'TALLA', 'TL', 1 ),
(curdate(), 1, CURDATE(), 1, 2, 'CENTÍMETROS', 'CM', 1 ),
(curdate(), 1, CURDATE(), 1, 3, 'MILÍMETROS', 'MM', 1 );
(curdate(), 1, CURDATE(), 1, 4, 'UNIDADES', 'U', 1 );


-- Creación de divisiones genéricas
INSERT INTO ctg_divisiones (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, descripcion, estado_id, taller_id, tipo_catalogo_id)
VALUES
('2020-06-15', 1, '2020-06-15', 1, 'DIVISION GENERICA PRODUCTOS', 1, 1, 1),
('2020-06-15', 1, '2020-06-15', 1, 'DIVISION GENERICA SERVICIOS', 1, 1, 2);


-- Creación de categorías genéricas
INSERT INTO ctg_categorias (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, descripcion, estado_id, unidad_medida_id, division_id, permite_solicitud, precio_empresa, precio_empresa_id, precio_taller, precio_taller_id, costo_taller, prct_utilidad_empresa, prct_utilidad_taller, acabado, costo_piedras, datos_extra, escala_peso, parte_interna, proveedor, tiempos_entrega, valor_gramo_diferenciado, envio_material)
VALUES
('2020-06-15', '1', '2020-06-15', '1', 'CATEGORIA GENERICA PRODUCTOS', '1', '1', (select id_division from ctg_divisiones where descripcion = 'DIVISION GENERICA PRODUCTOS'), '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '1', '1', '1', '1', '1', '1'),
('2020-06-15', '1', '2020-06-15', '1', 'CATEGORIA GENERICA SERVICIOS', '1', '1', (select id_division from ctg_divisiones where descripcion = 'DIVISION GENERICA SERVICIOS'), '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '1');


-- Creación de producto y servicio genérico
INSERT INTO ctg_items (fecha_creacion, usuario_crea, fecha_modificacion, usuario_modifica, sku, descripcion, precio_taller, escala_peso, tiempo_entrega_min, tiempo_entrega_max, precio_empresa, categoria_id, estado_id, taller_id, tipo_catalogo_id, cantidad_piedras, costo_piedras, peso_max_dif, valor_gramo_dif, datos_extra, costo_taller, id_proveedor, prct_utilidad_empresa, prct_utilidad_taller, unidad_medida_id)
VALUES
('2020-06-15', '1', '2020-06-15', '1', 'PRO-GEN-001', 'PRODUCTO GENERICO', '0', '0.10', '0', '0', '0', (select id_categoria from ctg_categorias where descripcion = 'CATEGORIA GENERICA PRODUCTOS'), '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'),
('2020-06-15', '1', '2020-06-15', '1', 'SER-GEN-001', 'SERVICIO GENERICO', '0', '0', '0', '0', '0', (select id_categoria from ctg_categorias where descripcion = 'CATEGORIA GENERICA SERVICIOS'), '1', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1');


-- Creación de detalles para producto y servicio genérico
INSERT INTO ctg_detalleitems (fecha_creacion, usuario_crea, fecha_modificacion, peso_minimo, peso_maximo, cantidad_piedras, estado_id, id_item_id, medida, estandar, costo_piedras)
VALUES
('2020-06-04 23:09:53.269444', '17', '2020-06-04 23:09:53.269444', '0.00', '0.00', '0', '1', (select id_item from ctg_items where sku = 'PRO-GEN-001'), '0.00', 'AMERICANO', '0.00'),
('2020-06-04 23:09:53.269444', '17', '2020-06-04 23:09:53.269444', '0.00', '0.00', '0', '1', (select id_item from ctg_items where sku = 'SER-GEN-001'), '0.00', 'AMERICANO', '0.00');


-- crea permisos, asigna nuevos nombres y crea funciones


-- asigna permisos_talleres

INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_talleres'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_talleres'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_categorias'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_categorias'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_categorias'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_colores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_colores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_colores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_tallas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_tallas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_tallas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_items'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_items'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_items'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_adicionales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_adicionales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_adicionales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_solicitudtrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_solicitudtrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_ordentrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_ordentrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_piedras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_piedras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_piedras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'envio_sms'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'ver_detalle_costos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'ver_detalle_costos_sol'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_facturas'));


INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'env_reportes'));

INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_acabados'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_acabados'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_acabados'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_partesinternas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_partesinternas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_partesinternas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_anchuras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_anchuras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_anchuras'));



-- asigna permisos_operaciones
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_roles'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_paises'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_zonas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_zonas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_zonas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_sectores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_sectores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_sectores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_regiones'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_localidades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_localidades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_localidades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_ciudades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_ciudades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_ciudades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_proveedores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_configgeneral'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_configutilidadtaller'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_configutilidadproveedor'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_items'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_adicionales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_clientes'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_clientes'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_clientes'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_solicitudtrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_solicitudtrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_solicitudtrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_ordentrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_ordentrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_ordentrabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_piedras'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_preciosdefinidos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_categorias'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_categorias'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'ver_detalle_costos'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'ver_detalle_costos_sol'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_colores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_colores'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_facturas'));

INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_sociedades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_sociedades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_sociedades'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'view_tiendas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'add_tiendas'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'change_tiendas'));

INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'env_reportes'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'envio_reporte_user'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'prioridad_taller'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'envio_material_joyeria'));

-- permisos de fabricacion interna y fabricacion dividida
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'fabricacion_interna'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'fabricacion_dividida_ordenes'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN OPERACIONES'),(select id from auth_permission where codename = 'fabricacion_dividida_solicitudes'));








-- asigna permisos_administrador por país
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'add_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'change_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'view_usuarios'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'change_paises'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'view_configuracionapisms'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'change_configuracionapisms'));

INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'add_gruposempresariales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'change_gruposempresariales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'view_gruposempresariales'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'add_talleres'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'change_talleres'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'ADMINISTRADOR'),(select id from auth_permission where codename = 'view_talleres'));



-- cambia el nombre de los permisos

UPDATE auth_permission 
SET 
    name = REPLACE(name, 'Can ', '');
UPDATE auth_permission 
SET 
    name = REPLACE(name, 'add', 'Agregar');
UPDATE auth_permission 
SET 
    name = REPLACE(name, 'view', 'Ver');
UPDATE auth_permission 
SET 
    name = REPLACE(name, 'change', 'Modificar');




-- crea funcion_contador

DELIMITER $$
CREATE FUNCTION fn_contador() RETURNS int(11)
no sql
BEGIN
  SET @var := IFNULL(@var,0) + 1;
RETURN @var;
end$$
;


-- crea vista_zonas_taller

CREATE VIEW db_tsindri.vw_zonas_taller AS
    SELECT 
        FN_CONTADOR() AS id,
        a.id_zona AS id_zona,
        a.nombre AS nombre,
        b.id AS id_taller,
        b.nombre AS nombre_taller,
        a.pais_id AS pais_id
    FROM
        (ubc_zonas a
        JOIN usr_taller b)
    WHERE
        (a.pais_id = b.pais_id)
    ORDER BY a.pais_id , a.nombre , b.id
;


-- crea vista_zonas_proveedor

CREATE VIEW db_tsindri.vw_zonas_proveedor AS
    SELECT 
        FN_CONTADOR() AS id,
        a.id_zona AS id_zona,
        a.nombre AS nombre,
        b.id AS id_proveedor,
        b.nombres AS nombres,
        b.apellidos AS apellidos,
        a.pais_id AS pais_id
    FROM
        (ubc_zonas a
        JOIN prv_proveedores b)
    WHERE
        ((a.pais_id = b.pais_id)
            AND (b.tipo_usuario = 3)
            AND (a.id_zona = b.zona_id))
    ORDER BY a.pais_id , a.nombre , b.id
;


-- crea vist_sectores_taller

CREATE VIEW db_tsindri.vw_sectores_taller AS
    SELECT 
        FN_CONTADOR() AS id,
        a.id_sector AS id_sector,
        a.nombre AS nombre,
        b.id AS id_taller,
        b.nombre AS nombre_taller,
        a.pais_id AS pais_id

    FROM
        (ubc_sectores a
        JOIN usr_taller b)
    WHERE
        (a.pais_id = b.pais_id)
    ORDER BY a.pais_id , a.nombre , b.id
;


-- crea vista_operaciones_taller

CREATE VIEW db_tsindri.vw_operaciones_taller AS
    SELECT 
        FN_CONTADOR() AS id,
        a.id AS id_user,
        a.username AS username,
        b.id AS id_taller,
        b.nombre AS nombre_taller,
        a.pais_id AS pais_id
    FROM
        (usr_usuarios a
        JOIN usr_taller b)
    WHERE
        ((a.pais_id = b.pais_id)
            AND (a.tipo_usuario_id = 3))
    ORDER BY a.pais_id , a.username , b.id
;


-- crea vista_operaciones_proveedores

CREATE VIEW db_tsindri.vw_operaciones_proveedor AS
    SELECT 
        FN_CONTADOR() AS id,
        a.id AS id_user,
        a.username AS username,
        b.id AS id_proveedor,
        b.nombres AS nombres,
        b.apellidos AS apellidos,
        a.pais_id AS pais_id
    FROM
        (usr_usuarios a
        JOIN prv_proveedores b)
    WHERE
        ((a.pais_id = b.pais_id)
            AND (a.tipo_usuario_id = 3)
            AND (b.tipo_usuario = 3)
            AND (a.zona_id = b.zona_id))
    ORDER BY a.pais_id , a.username , b.id;



INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'view_divisiones'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'change_divisiones'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'add_divisiones'));


INSERT INTO cfg_configuracionsistema(id, clave, valor, observacion) VALUES (1,'PESO_MAX_IMAGEN','10','Medido en MB'),(2,'PESO_MAX_ARCHIVO','20','Medido en MB'),(3,'EXT_PERMITIDAS_IMAGEN','/(.jpg|.jpeg|.png)$/i','expresion regular'),(4,'EXT_PERMITIDAS_ARCHIVO','/(.jpg|.jpeg|.png|.pdf)$/i','expresion regular');

-- Configuración API SMS
INSERT INTO cfg_configuracionapisms(clave, valor, observacion, pais_id) VALUES ('URL_TOKEN',' ',NULL,1);
INSERT INTO cfg_configuracionapisms(clave, valor, observacion, pais_id) VALUES ('client_id',' ',NULL,1);
INSERT INTO cfg_configuracionapisms(clave, valor, observacion, pais_id) VALUES ('client_secret',' ',NULL,1);
INSERT INTO cfg_configuracionapisms(clave, valor, observacion, pais_id) VALUES ('URL_ENVIO_LISTA',' ',NULL,1);
INSERT INTO cfg_configuracionapisms(clave, valor, observacion, pais_id) VALUES ('CONTENIDO_SMS',' ',NULL,1);


-- Colores proveedor
insert into ctg_coloresproveedor (proveedor_id, color_id, costo_adicional)
(select pr.id, cl.id_color, 0 from prv_proveedores pr
inner join ctg_colores cl
on pr.taller = cl.taller_id)


-- franklin
INSERT INTO cfg_configuracionsistema(clave, valor, observacion) VALUES ('CANTIDAD_MAX_IMAGENES', 2, 'cantidad maxima de imagenes');
-- permisos para las acciones de ordenes, iniciar y finalizar trabajo
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'iniciar_orden'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'finalizar_trabajo'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'anular_orden'));
INSERT INTO auth_group_permissions(GROUP_ID, PERMISSION_ID) values ((select id from auth_group where name = 'NN_ADMINISTRADOR_ADMIN TALLER'),(select id from auth_permission where codename = 'enviar_producto'));



-- insert para nuevas notas de ayuda (agregadas aparte de las que ya se registran de la configuracion base)
INSERT INTO trn_ConfiguracionTooltipOperaciones(campo_orden, estado, texto) VALUES ('solicitud_detalle', 1, '');
INSERT INTO trn_ConfiguracionTooltipOperaciones(campo_orden, estado, texto) VALUES ('color', 1, '');




