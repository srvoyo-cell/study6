function ajaxStart(){
$.ajax({
    type: 'post',
    url:  'start.php',
    dataType: "html",
    //data: jQuery.param({ iterations: "10000", field2 : "hello2"}) ,
    data: jQuery.param({ iterations: $('#iterations').val()}) ,
    success: function(result){
        $("#text2").html(result);
        t = 0;
        document.getElementById("calculations").value = 0;
        
        document.getElementById("deletebutton").disabled = true;
        document.getElementById("iterbutton").disabled = true;
        document.getElementById("startbutton").disabled = true;
        document.getElementById("stopbutton").textContent = "Остановить";
        timerId = setInterval(() => checkresult(), 1000);
        
        
/*var obj = $("#times");
var start = 0;
setTimer = setInterval(function () {
start+=1;
obj.val(start);
}, 1000);*/
    }
});
}