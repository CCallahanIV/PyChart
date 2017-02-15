$(document).ready(function(){
    $('.dataLink').on("click", function(event){
        event.preventDefault();
        console.log("Making AJAX call.")
        $.ajax({
            method: 'GET',
            url: $(this).attr('href'),
            success: function(data){
                console.log(JSON.parse(data))
                f_data = JSON.parse(data)
                $('#table').bootstrapTable('refreshOptions', {'columns': f_data['columns']})
                $('#table').bootstrapTable('load', f_data['data'])
            }
        });        
    });
});
