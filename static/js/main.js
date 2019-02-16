

function delete_bookmark(bookmarkId) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data ={"id": bookmarkId, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/dashboard/delete_bookmark", function(){
        $("#"+data["id"]).hide("slow", function(){ $(this).remove(); })
    });
}

function save_bookmark(bookmarkId) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data ={"id": bookmarkId, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/dashboard/mark_bookmark", function(){
        //$("#"+data["id"]).fadeOut("slow", function(){ $(this).remove(); })
        // Check if class already is set first
        $(".link-save-button").addClass("bookmark-read");
    });
}


function generate_telegram_code() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var telegram_username = $("#telegram_username").val();
    var data ={"telegram_username": telegram_username, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/settings/telegram", function(result){
        $("#secretcode .token").text(result["token"]);
        $("#secretcode").removeClass("invisible");
    });
}


function send_ajax(data, url, callback) {
	$.ajax({
		type : "POST",
        url : url,
        data: data,
		success: callback,
		error: function(error) {
            console.log("Error doing ajax request...");
            console.log(error);
		}
	});
}