

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


function delete_bookmark(bookmarkId) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data ={"bm_id": bookmarkId, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/dashboard/delete_bookmark", function(){
        $("#"+data["bm_id"]).hide("slow", function(){ $(this).remove(); })
    });
}

// Archives bookmark
function save_bookmark(bookmarkId) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data ={"bm_id": bookmarkId, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/dashboard/mark_bookmark", function(){
        //$("#"+data["id"]).fadeOut("slow", function(){ $(this).remove(); })
        $("#"+bookmarkId+" .link-save-button").toggleClass("bookmark-read");
    });
}

function add_bookmark() {
    var bookmark = $("[name=add_bookmark_input]").val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data ={"data": bookmark, "csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/dashboard/add_bookmark", function(){
        $("#add_bookmark_result").show(600).delay(2300).fadeOut(1200);
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