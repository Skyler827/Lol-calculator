// This js file does three things:
// 1 makes modal divs into jQuery dialogs
// 2 makes links open the dialogs
// 3 makes selections in the dialogs select the champs and closes the dialogs

$(function() {
    var champ_ids_names = [];
    $.ajax({url:"/champ_id_names", success: function(result){
        champ_ids_names = result;
    }});
    function make_champ_select(color) {
        var champ_select = document.createElement("div");
        champ_select.id = color+"-champ-select";
        champ_select.classList.add("my-modal");
        champ_select.classList.add("champ-select-modal");
        var p_tag = document.createElement("p");
        p_tag.innerHTML = "Select a champion:";
        champ_select.appendChild(p_tag);

        for (let i=0; i< champ_ids_names.length; i++) {
            let div = document.createElement("div");
            div.classList.add("selectable");
            div.classList.add("selectable-champ");
            let img = document.createElement("img");
            img.src = "static/calc/img/champ_square/"+champ_ids_names[i][0]+".png";
            div.appendChild(img);
            let champ_p_tag = document.createElement("p");
            let a_tag = document.createElement("a");
            a_tag.text = champ_ids_names[i][1];
            a_tag.appendChild(document.createElement("span"));
            champ_p_tag.appendChild(a_tag);
            div.appendChild(champ_p_tag);
            champ_select.appendChild(div);

            $(a_tag).click(function(_) {
                let champ_path = "/static/calc/img/champ_square/"+champ_ids_names[i][0]+".png";
                $("."+color+"-champ .inner-champ-div .champ-icon").attr("src", champ_path);
                $("."+color+"-champ .inner-champ-div .clickable-image-container div.middle").hide();
                $("."+color+"-champ .inner-champ-div p.champ-name").text(champ_ids_names[i][1]);
                $("input.run-combat-submit").click();
                $(champ_select).dialog("close");
            });
        }
        var empty_div = document.createElement("div");
        champ_select.appendChild(empty_div);
        $(champ_select).dialog({
            title: "Select "+color+" Side Champion",
            width: 0.7 * window.innerWidth,
            autoOpen: true,
            modal: true,
            draggable: false,
            resizable: false,
            maxHeight: document.documentElement.clientHeight-20,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            appendTo: "body"
        });
        return champ_select;
    }

    $(window).resize(function() {
        $("#red-champ-select").dialog("option", "width", 0.7*window.innerWidth);
        $("#blue-champ-select").dialog("option", "width", 0.7*window.innerWidth);
    });
    //make links open the dialogs:
    $(".blue-champ .inner-champ-div a.clickable-image-container").click(function(e) {
        make_champ_select("blue");
    });
    $(".red-champ .inner-champ-div a.clickable-image-container").click(function(e) {
        make_champ_select("red");
    });

});