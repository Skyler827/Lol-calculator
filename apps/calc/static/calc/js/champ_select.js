// This js file does three things:
// 1 makes modal divs into jQuery dialogs
// 2 makes links open the dialogs
// 3 makes selections in the dialogs select the champs and closes the dialogs

$(function() {
    // make elements dialogs:
    $("#blue-champ-select").dialog({
        title: "Select Blue Side Champion",
        width: 0.7*window.innerWidth,
        autoOpen: false,
        modal: true,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );
            }
        }
    });
    $("#red-champ-select").dialog({
        title: "Select Red Side Champion",
        width: 0.7*window.innerWidth,
        autoOpen: false,
        modal: true,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );
            }
        }
    });
    $(window).resize(function() {
        $("#red-champ-select").dialog("option", "width", 0.7*window.innerWidth);
        $("#blue-champ-select").dialog("option", "width", 0.7*window.innerWidth);
    });
    //make links open the dialogs:
    $(".blue-champ a.clickable-image-container").click(function(e) {
        $("#blue-champ-select").dialog("open");
    });
    $(".red-champ a.clickable-image-container").click(function(e) {
        $("#red-champ-select").dialog("open");
    });

    //make items in dialog set the champs and close the dialog
    $("#blue-champ-select .selectable-champ a").click(function(e) {
        let champName = e.currentTarget.innerText;
        let champ_path = "/static/calc/img/champ_square/"+champName+".png";
        $(".blue-champ .champ-icon").attr("src", champ_path);
        $(".blue-champ .clickable-image-container div.middle").hide();
        $(".blue-champ p.champ-name").text(champName);
        $("#blue-champ-select").dialog("close")

    });
    $("#red-champ-select .selectable-champ a").click(function(e) {
        let champName = e.currentTarget.innerText;
        let champ_path = "/static/calc/img/champ_square/"+champName+".png";
        $(".red-champ .champ-icon").attr("src", champ_path);
        $(".red-champ .clickable-image-container div.middle").hide();
        $(".red-champ p.champ-name").text(champName);
        $("#red-champ-select").dialog("close")
    });
});