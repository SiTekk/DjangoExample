jQuery(function() 
{
   setTimeout(clock, 1000);
});

function clock() 
{
    var d = new Date();
    var t = d.toLocaleTimeString();
    jQuery("#clock").html(t);
    setTimeout(clock, 1000);
}