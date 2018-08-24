$(function() {
    var items = [];
    $.ajax("/item_ids", {success: (function(data){
        items = data;
    })});
    function popup_item_selector(target) {
        var item_selector = document.createElement("div");
        item_selector.id = "item-selector";
        item_selector.classList.add("my-modal");
        item_selector.classList.add("item-selector-modal");

        // TODO: write a django view to get all items as json
        //       then write an ajax request for that list
        // in the meantime, here are some haredcoded item ids that we will show:
        $(item_selector).dialog({
            title: "Select an item:",
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
            position: {
                at: "center top"
            },
            appendTo: "body"
        });
        for (let i=0; i< items.length; i++) {
            let div = document.createElement("div");
            div.classList.add("selectable");
            div.classList.add("selectable-item");
            let img = document.createElement("img");
            img.src = "/static/calc/img/items/"+items[i][0]+".png";
            div.appendChild(img);
            let item_name = document.createElement("p");
            let inner_link = document.createElement("a");
            inner_link.textContent = items[i][1];
            let inner_span = document.createElement("span");
            inner_link.appendChild(inner_span);
            item_name.appendChild(inner_link);
            div.appendChild(item_name);
            item_selector.appendChild(div);

            $(inner_link).click(function(e){
                let src = "/static/calc/img/items/"+items[i][0]+".png"
                console.log(src);
                $(target).find("img").attr("src", src);
                $(item_selector).dialog("close");
            });
        }
    }
    $(".item-outerdiv").click(function(event) {
        popup_item_selector(event.currentTarget);
    });

});