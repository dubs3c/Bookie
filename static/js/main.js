
function filterOnTags(tag){
    var list = [];
    $(".tags span").map(function() {
        if ($(this).hasClass("tag-active")) {
            list.push(encodeURIComponent(this.innerHTML));
        }
    });
    var query = list.join("|");
    var url = new URL(window.location.href);
    url.searchParams.set("tags", query);
    window.location.replace(url);
}


function getFilterTagsFromURL(sParam="tags") {
    var query = "";
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split("&");
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split("=");
        if (sParameterName[0] === sParam) {
            query = decodeURIComponent(sParameterName[1]);
            break;
        }
    }
    return decodeURIComponent(query).split("|");
}


function setTagsFromURL() {
    var tags = getFilterTagsFromURL();
    $(".tag-button").map(function() {
        var key = $(this).html();
        if (key) {
            if (tags.includes(key)) {
                $(this).addClass("tag-active");
            }
        }
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

function addBookmark() {
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

function deleteUser() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var userID = $(".modal-body input").val()
    var data = {"csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/settings/users/"+userID+"/delete", function(result){
        location.reload();
    });
}

function deactivateUser(userid) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var data = {"csrfmiddlewaretoken": csrftoken};
    send_ajax(data, "/settings/users/"+userid+"/deactivate", function(result){
        location.reload();
    });
}

$(document).ready(function() {

     $(".infinitive-scroll").infiniteScroll({
        // options
        path: ".pagination__next",
        append: ".postcard",
        history: false,
        status: ".page-load-status",
        hideNav: ".pagination"
    });

    $(".tag-button").click(function() {
        $(this).toggleClass("tag-active");
    });

    setTagsFromURL();

    $('#deleteUserModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var username = button.data('username');
        var userID = button.data('userid');
        var modal = $(this);
        modal.find('.modal-body span').text(username);
        modal.find('.modal-body input').val(userID);
      })

});