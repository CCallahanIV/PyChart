$(document).ready(function(){
    $('#scatter').hide()

    function display_selects(chart_type){
        if(chart_type === "scatter"){
            $('#scatter').show()
            $('#barHistogram').hide()
        } else {
            $('#scatter').hide()
            $('#barHistogram').show()
        }
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

    $('#renderBtn').on("click", function(event){
        event.preventDefault()
        var table_data = $('.table').bootstrapTable('getData')
        var form_data = {};
        $("form").serializeArray().map(function(x){form_data[x.name] = x.value;}); 
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
        display_selects($(this).val())
    });

});
