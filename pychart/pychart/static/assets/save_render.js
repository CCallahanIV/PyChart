$(document).ready(function(){
    $('#saveBtn').on('click', function(event){
        event.preventDefault()
        var render_data = {};
        $('.renderForm').serializeArray().map(function(x){
            render_data[x.name] = x.value;
        });
        render_data["html"] = sessionStorage.getItem('render_html')
        render_data["render_type"] = $('#chartType').val();
        sessionStorage.removeItem('render_html')
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