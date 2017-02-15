$(document).ready(function(){
    $('#saveBtn').on('click', function(event){
        event.preventDefault()
        var render_data = {};
        $('.renderForm').serializeArray().map(function(x){
            render_data[x.name] = x.value;
        });
        render_data["html"] = $('.renderContainer').html();
        render_data["render_type"] = $('#chartType').val();
        console.log(render_data)
        $.ajax({
            method: 'POST',
            url: '/data/render/create/',
            data: JSON.stringify(render_data),
            contentType: 'application/json',
            success: function(response){
                window.location.replace(response.url)
            }
        });
    });
});