*****************
**Modelos usr**
*****************

Dentro de la carpeta **usr** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación usr

Modelo TipoUsuarios
======================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para registrar los tipos de usuarios que existen en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_tipo_usuario", "Id del tipo de usuario."
        "tipo_usuario","Clave del tipo de usuario."
        "descripcion", "Descripción del tipo de usuario."

Modelo Taller
======================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para registrar talleres en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "pais", "Id del país al que pertenece el taller."
        "nombre","Nombre del taller."
        "valor_fraccion", "Valor del gramo de fabricación para el taller."
        "costo_gramo_base", "Valor de gramo de materia prima."
        "utilidad_sobre_fabricacion", "Porcentaje de utilidad que se aplica sobre los costos de fabricación."
        "utilidad_sobre_base", "Porcentaje de utilidad que se aplica sobre el costo de la materia prima."
        "utilidad_sobre_piedras", "Porcentaje de utilidad que se aplica sobre el costo de piedras."
        "utilidad_sobre_adicionales", "Porcentaje de utilidad que se aplica sobre el costo de los adicionales."
        "porcentaje_merma", "Porcentaje de merma que maneja el taller."
        "prct_impuestos", "Porcentaje de impuestos que se aplica sobre las fabricaciones."
        "tmp_resp_sol", "Tiempo límite para responder una solicitud."
        "escala_peso", "Escala de peso en la que puede ser fabricado un ítem."
        "estandar_tallas", "Estandar de tallas que maneja el taller."
        "configurado", "Indica si el taller ya ha sido configurado."
        "externo", "Indica si se trata de un taller externo o interno."

Modelo Roles
======================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para registrar los roles de usuario disponibles en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_rol", "Id del rol registrado."
        "descripcion","Descripción del rol."
        "estado", "Id del estado del rol puede ser activo o inactivo."
        "tipo_usuario", "Id del tipo de usuario al que pertenece el rol."
        "conf_general", "Id de la empresa a la que pertenece el rol."
        "taller", "Id del taller al que pertenece el rol."
        "admin", "Indica si se trata de un rol de administrador."
        "zonal", "Indica si se trata de un rol de jefe zonal."
        "pais", "Id del país al que pertenece el rol."
        "grupo", "Id del grupo al que pertenece el rol."

Modelo Usuarios
================

Modelo de tipo abstracto que hereda de ``AbstractUser``. Este es el modelo para el manejo de los usuarios que se registran en el sistema, a los campos que ya incluye el modelo que crea Django por defecto se adicionan los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "tipo_usuario", "Id del tipo de usuario al que pertenece."
        "rol", "Id del rol asignado al usuario."
        "pais","Id del país al que pertenece el usuario."
        "ciudad", "Id de la ciudad a la que pertenece el usuario."
        "zona", "Id de la zona a la que pertenece el usuario."
        "sector", "Id del sector al que pertenece el usuario."
        "direccion", "Dirección del usuario."
        "telefono", "Teléfono del usuario."
        "observacion", "Observación sobre el usuario."
        "img_perfil", "Url de la imagen de perfil para el usuario."
        "tmp_lim_vta", "Tiempo límite en que puede finalizar una órden de trabajo."
        "aut_externo", "Indica si el usuario tiene permitido generar solicitudes con externos."
        "taller", "Id del taller al que pertenece el usuario."
        "config_gen", "Id de la empresa a la que pertence el usuario."
        "nueva_clave", "Indica si el usuario ingresa por primera vez después de creado o reestablecida la contraseña."
        
Modelo UsuariosGrupos
======================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para la asignación de grupo para un usuario, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "usuarios","Id del usuario."
        "group", "Id del grupo que se le asigna al usuario."

Modelo GruposPermisos
======================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para la aignación de permisos que posee un grupo, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "group","Id del grupo de usuarios."
        "permission", "Id del permiso asignado al grupo."
