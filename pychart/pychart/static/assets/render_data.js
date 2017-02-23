$(document).ready(function(){
    //Initial form setup.
    $('#Scatter').hide()
    $('#Histogram').hide()
    $('.renderForm').hide()

    //Helper function for displaying correct chart form.
    function display_form(chart_type){
        $('.chartForm').hide()
        $('#' + chart_type).show()
    };

    //Event Handler for rendering chart from table data.
    $('.renderBtn').on("click", function(event){
        event.preventDefault()
        $('.renderForm').show();
        var table_data = $('.table').bootstrapTable('getData');
        var form_data = {};
        $($(this).parent()).serializeArray().map(function(x){form_data[x.name] = x.value;});
        var chart_type = $(this).parent().attr('data');
        form_data["chart_type"] = chart_type;
        $.ajax({
            method: 'POST',
            url: '/data/retrieve/render/',
            data: JSON.stringify({"table_data": table_data, "form_data": form_data}),
            contentType: 'application/json',
            success: function(result){
                $('.renderContainer').html(result)
                sessionStorage.setItem('render_html', result)
            }
        });        
    });

    //Event handler for displaying correct chart form.
    $('#chartType').on("change", function(){
        display_form($(this).val())
    });

});
