$(function() {
    function modal_summoner_spell_factory(color, key, target) {
        console.log(target);
        // Define the modal
        var summ_selector = document.createElement("div");
        summ_selector.id = "summoner-spell-selector-"+color+"-"+key;
        summ_selector.classList.add("my-modal");
        summ_selector.classList.add("summoner-spell-modal");
        var p_tag = document.createElement("p");
        p_tag.innerHTML = "Select a summoner spell:";
        summ_selector.appendChild(p_tag);
        var spell_names = [
            "Barrier", "Exhaust", "Ignite", "Flash", "Heal", "Smite", "Teleport", "Cleanse"];
        $(summ_selector).dialog({
            title: "Select "+color+" Side Summoner spell on key "+key+"",
            width: 0.7 * window.innerWidth,
            autoOpen: true,
            modal: true,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            appendTo: "body"
        });
    
        for (let i=0; i<spell_names.length; i++) {
            // Define the summoner spells
            let div = document.createElement("div");
            div.classList.add("selectable");
            div.classList.add("selectable-summ");
            let img = document.createElement("img");
            img.src = "static/calc/img/summoner/Summoner"+spell_names[i]+".png";
            div.appendChild(img);
            let p_label = document.createElement("p");
            let a_tag = document.createElement("a");
            a_tag.text = spell_names[i];
            a_tag.appendChild(document.createElement("span"));
            p_label.appendChild(a_tag);
            div.appendChild(p_label);
            summ_selector.appendChild(div);

            $(a_tag).click(function(_){
                $(target).find("img").attr("src", "/static/calc/img/summoner/Summoner"+spell_names[i]+".png");
                $(target).find(".middle").text("")
                $(summ_selector).dialog("close");
            });
        }
        return summ_selector;
    }
    // make links open dialogs:
    $(".blue-champ .summ-outerdiv-D a").click(function(e) {
        modal_summoner_spell_factory("blue", "D", e.currentTarget);
    });
    $(".blue-champ .summ-outerdiv-F a").click(function(e) {
        modal_summoner_spell_factory("blue", "F", e.currentTarget);
    });
    $(".red-champ .summ-outerdiv-D a").click(function(e) {
        modal_summoner_spell_factory("red", "D", e.currentTarget);
    });
    $(".red-champ .summ-outerdiv-F a").click(function(e) {
        modal_summoner_spell_factory("red", "F", e.currentTarget);
    });
});