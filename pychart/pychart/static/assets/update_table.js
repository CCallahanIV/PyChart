$(document).ready(function(){

    function reset_charts(){
        $('.columnSelect').empty()
        $('.nullable').append('<option>','')
    };

    function add_columns(columns){
        var select_boxes = $('.columnSelect');
        reset_charts()
        for(i=0; i < columns.length; i++){
            select_boxes.append($('<option>', {"value": columns[i]["field"], "text": columns[i]["title"]}));
        }
    };

    $('.dataLink').on("click", function(event){
        event.preventDefault();
        $.ajax({
            method: 'GET',
            url: $(this).attr('href'),
            success: function(data){
                f_data = JSON.parse(data)
                $('#table').bootstrapTable('refreshOptions', {'columns': f_data['columns']})
                $('#table').bootstrapTable('load', f_data['data'])
                add_columns(f_data['columns'])
            }
        });        
    });
});
