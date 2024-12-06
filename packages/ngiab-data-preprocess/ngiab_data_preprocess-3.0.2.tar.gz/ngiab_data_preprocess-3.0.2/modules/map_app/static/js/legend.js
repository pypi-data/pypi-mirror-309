// wait for the DOM to finish loading
document.addEventListener('DOMContentLoaded', function () {
    // load in html template for the control panel
    $(".custom_legend").load("static/html/legend.html", function() {
        // defaults 
        $(".leaflet-marker-pane").toggle(200);
        $(".leaflet-shadow-pane").toggle(200);
        $("#legend_nexus_circles_icon").toggleClass("turned_off");
    });

    $(".custom_legend").click(function (f) {
        // stop the map click event from firing        
        if (f.target.classList.contains("legend_icon")) {
            $("#" + f.target.id).toggleClass("turned_off");
        }
        if (f.target.id === "legend_selected_cat_layer_icon") {
            $(".selected-cat-layer").toggle(200);
        }
        if (f.target.id === "legend_upstream_layer_icon") {
            $(".upstream-cat-layer").toggle(200);
        }
        if (f.target.id === "legend_to_cat_icon") {
            $(".flowline-to-cat-layer").toggle(200);
        }
        if (f.target.id === "legend_to_nexus_icon") {
            $(".flowline-to-nexus-layer").toggle(200);
        }
        if (f.target.id === "legend_nexus_circles_icon") {
            //$(".nexus-layer").toggle(200);
            // using the full pane is way faster
            $(".leaflet-marker-pane").toggle(200);
            $(".leaflet-shadow-pane").toggle(200);
        }
        if (f.target.id === "high_contrast") {
            $("body").toggleClass("high-contrast");
            console.log(f.target.id);
            console.log(f.target);
        }

        // disable propagation to prevent map click event from firing
        f.stopPropagation();
        return;

    });

});



