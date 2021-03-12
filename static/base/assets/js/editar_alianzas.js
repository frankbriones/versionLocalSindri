$(document).ready(function(){
    $('.loader').hide();
})

function obtener_colores(item){
    var item_id = item;
    var parametros = {
        'item_id': item_id
    };
    colores_item(parametros);
}

function colores_item(parametros){
    $.ajax({
        url: '/catalogo/obtener/colores_item/ajax/',
        type: 'GET',
        data: parametros,

        success: function(data){
            let colores = data.color_id;
            let colores_descripcion = data.color_descripcion
            $('#id_colores').val(colores);
            let ul_colores = $('.select2-selection__rendered');
            ul_colores.attr("id", "ul_colores")
            $('#ul_colores').html(data.colores_html)
        }
    })
}

