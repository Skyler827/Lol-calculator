$(function() {
    $("select.level-selector").each(function(index) {
        for (let i=1; i<= 18; i++) {
            $(this)[0]
            var option = document.createElement("option");
            option.innerText = i;
            option.value = i;
            $(this)[0].appendChild(option)
        }
        
    });
});