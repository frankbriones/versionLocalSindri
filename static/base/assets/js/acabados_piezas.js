$(document).ready(function(){
    $('.loader').hide();
})
// obtener acabados de alianzas


function obtener_acabados(item){
    var item_id = item;
    var parametros = {
        'item_id': item_id
    };
    acabados_piezas(parametros);
}

function acabados_piezas(parametros){
    $.ajax({
        url: '/catalogo/obtener/acabados_item/ajax/',
        type: 'GET',
        data: parametros,

        success: function(data){
            console.log(data.acabados_html)
            let acabados = data.acabados_id;
            $('#id_acabados').val(acabados);
            let ul_acabados = $('.select2-selection__rendered'); 
            ul_acabados.attr("id", "ul_acabados")
            $('#ul_acabados').html(data.acabados_html)
        }
    })
}
