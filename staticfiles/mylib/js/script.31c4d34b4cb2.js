$(document).ready(function(){
    $("#comments").on("click", ".reply", function(event){
        event.preventDefault();
        var form = $("#postcomment").clone(true);
        form.find('.parent').val($(this).parent().parent().attr('id'));
        $(this).parent().append(form);
    });
});

console.log("Test");