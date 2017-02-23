$(document).ready(function(){

    //TODO: This function duplicates update_table.js.  Use conditional for add_columns method and use same function for both pages?
    $('.dataLink').on("click", function(event){
        event.preventDefault();
        $.ajax({
            method: 'GET',
            url: $(this).attr('href'),
            success: function(data){
                f_data = JSON.parse(data)
                $('#table').bootstrapTable('refreshOptions', {'columns': f_data['columns']})
                $('#table').bootstrapTable('load', f_data['data'])
            }
        });        
    });
});
