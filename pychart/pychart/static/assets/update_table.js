$(document).ready(function(){
    $('.dataLink').on("click", function(event){
        event.preventDefault();
        $.ajax({
            method: 'GET',
            url: $(this).attr('href'),
            success: function(){
                $('table').bootstrapTable()
            }
        });        
    });
});
