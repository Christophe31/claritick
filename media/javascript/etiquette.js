var etiquette_print_dialog;
function get_print_dialog(get_etiquette_form_url, app, model, object_id)
{
    if ( ! etiquette_print_dialog )
    {
        etiquette_print_dialog = new dijit.Dialog(
        {
            title: "impression d'étiquette",
            style: "width: 300px"
        });
    }
    
    etiquette_print_dialog.set("Chargement...");
    dojo.xhrGet(
    {
        url: get_etiquette_form_url,
        content: {
            "model": model,
            "app": app
        },
        handleAs: "text",
        load: function(data) 
        {
            etiquette_print_dialog.set('content', data);
            var printer_form = dojo.byId('printer_form');
            dojo.create("input", {
                "type": "hidden",
                "name": "obj_pk",
                "value": object_id
            }, printer_form, "last");
            dojo.connect(printer_form, "onsubmit", function(event) 
            {
                dojo.stopEvent(event);
                dojo.xhrPost(
                {
                    form: printer_form,
                    handleAs: "text",
                    load: function(post_data) 
                    {
                        etiquette_print_dialog.set('content', post_data);
                    },
                    error: function(error) { console.error("Error: "+error); }
                });
            });
        },
        error: function(error) { console.error("Error: "+error); }
    });
    return etiquette_print_dialog;
}
