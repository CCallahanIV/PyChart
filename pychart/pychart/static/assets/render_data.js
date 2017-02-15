$(document).ready(function(){

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
        var data = $('.table').bootstrapTable('getData')
        $.ajax({
            method: 'POST',
            url: '/data/retrieve/render/',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(result){
                
            }
        });        
    });
});
