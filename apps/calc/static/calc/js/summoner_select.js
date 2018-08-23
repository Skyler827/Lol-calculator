$(function() {
    function make_summoner_spell_modal(color, key) {
        // Define the modal
        var summ_selector = document.createElement("div");
        summ_selector.id = "summoner-spell-selector-"+color+"-"+key;
        summ_selector.classList.add("my-modal");
        summ_selector.classList.add("summoner-spell-modal");
        var p_tag = document.createElement("p");
        p_tag.innerHTML = "Select a champion:";
        summ_selector.appendChild(p_tag);
        var spell_names = [
            "Barrier", "Exhaust", "Flash", "Heal", "Smite", "Teleport"];
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
            div.appendChild(champ_p_tag);
            summ_selector.appendChild(div);

            $(a_tag).click(function(_){
                console.log("ayo");
            });
        }
    }
    console.log("ayy");
});