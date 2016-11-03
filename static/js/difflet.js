//$(".dph").click(function() {console.log($(this).data("id")) })
//$(".h .leftPane").slideToggle('slow');$(".h .rightPane").slideToggle('slow');
$(".dp").click(function() {
    i=$(this).data("id");
    $(".row"+ i+" .leftPane").slideToggle('slow');
    $(".row"+i+" .rightPane").slideToggle('slow'); }
);
