$(document).ready(function(){
    $('#Scatter').hide()
    $('#Histogram').hide()
    $('.renderForm').hide()

    function display_form(chart_type){
        $('.chartForm').hide()
        $('#' + chart_type).show()
    };

    //Below function taken from http://stackoverflow.com/questions/16789988/how-to-write-a-django-view-for-a-post-request
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

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
                console.log("rendering", result)
                $('.renderContainer').html(result)
            }
        });        
    });

    $('#chartType').on("change", function(){
        display_form($(this).val())
    });

});
