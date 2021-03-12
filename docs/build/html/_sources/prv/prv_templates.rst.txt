*******************
**Templates prv**
*******************

Dentro de la carpeta **prv** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación prv correspondiente a la creación, consulta y modificación de proveedores en el sistema.

Template actualizar_proveedor_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un proveedor, las funciones que posee este template son las siguientes:

Función actualizarProveedor
-----------------------------

Realiza una petición de tipo POST a la :ref:`url proveedores_actualizar` enviando como parámetro el id del proveedor a actualizar.

Template proveedores_form
==========================

Template de la pantalla que permite crear o editar un proveedor para un país determinado, realiza una petición de tipo POST a la :ref:`url proveedores_crear` en caso de creación de un proveedor, y una petición de tipo POST a la :ref:`url proveedores_editar` en caso de modificar los datos de un proveedor enviando como parámetro el id del proveedor a editar.

Template proveedores_lista
===========================

Template de la pantalla para consultar todos los que pertenezcan al mismo país o taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_proveedor_modal` y a la pantalla de creación o edición de proveedores :ref:`Template proveedores_form`. Para la consulta de los proveedores se realiza una petición de tipo GET a la :ref:`url proveedores_lista`.
