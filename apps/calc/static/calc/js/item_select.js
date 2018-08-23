$(function() {
    function popup_item_selector(target) {
        var item_selector = document.createElement("div");
        item_selector.id = "item-selector";
        item_selector.classList.add("my-modal");
        item_selector.classList.add("item-selector-modal");

        // TODO: write a django view to get all items as json
        //       then write an ajax request for that list
        // in the meantime, here are some haredcoded item ids that we will show:
        items = [
            {
                id: "2055",
                name: "Control Ward",
            }, {
                id:"3006",
                name: "Bezerkers Greaves",
            },{
                id:"3031",
                name: "Infinity Edge",
            }, {
                id:"3046",
                name: "Phantom Dancer",
            }, {
                id:"3072",
                name: "The Bloodthirster",
            }, {
                id:"3085",
                name:"Runaan's Hurricane",
            }, {
                id:"3092",
                name:"Reminant of the Watchers",
            }, {
                id:"3095",
                name:"Stormrazor",
            }, {
                id:"3107",
                name: "Redemption"
            }, {
                id:"3158",
                name:"Ionian Boots of Lucidity",
            }, {
                id:"3174",
                name: "Athene's Unholy Grail",
            }, {
                id:"3504",
                name: "Ardent Censor"
            }
        ];
        $(item_selector).dialog({
            title: "Select an item:",
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
        for (let i=0; i< items.length; i++) {
            let div = document.createElement("div");
            div.classList.add("selectable");
            div.classList.add("selectable-item");
            let img = document.createElement("img");
            img.src = "/static/calc/img/items/"+items[i].id+".png";
            div.appendChild(img);
            let item_name = document.createElement("p");
            let inner_link = document.createElement("a");
            inner_link.textContent = items[i].name;
            let inner_span = document.createElement("span");
            inner_link.appendChild(inner_span);
            item_name.appendChild(inner_link);
            div.appendChild(item_name);
            item_selector.appendChild(div);

            $(inner_link).click(function(e){
                $(target).find("img").attr("src", "/static/calc/img/items/"+items[i].id+".png");
                $(item_selector).dialog("close");
            });
        }
    }
    $(".item-outerdiv").click(function(event) {
        console.log("ayyy");
        popup_item_selector(event.currentTarget);
    });

});