
$(function(){
  if($('body').hasClass('bookmark-detail')){

    function send_ajax(type, data, url, callback) {
      $.ajax({
        type : type,
        url : url,
        data: data,
        beforeSend: function(xhr){xhr.setRequestHeader('X-CSRFToken', data["csrfmiddlewaretoken"]);},
        success: callback,
        error: function(error) {
                console.log("Error doing ajax request...");
                console.log(error);
        }
      });
    }
    
    const tagContainer = document.querySelector('.tag-container');
    const input = document.querySelector('.tag-container input');
    
    let tags = [];
    
    function createTag(label) {
      const div = document.createElement('div');
      div.setAttribute('class', 'tag');
      const span = document.createElement('span');
      span.innerHTML = label;
      const closeIcon = document.createElement('i');
      closeIcon.innerHTML = 'x';
      closeIcon.setAttribute('class', 'material-icons');
      closeIcon.setAttribute('data-item', label);
      div.appendChild(span);
      div.appendChild(closeIcon);
      return div;
    }
    
    function clearTags() {
      document.querySelectorAll('.tag').forEach(tag => {
        tag.parentElement.removeChild(tag);
      });
    }
    
    function addTags() {
      clearTags();
      tags.slice().reverse().forEach(tag => {
        tagContainer.prepend(createTag(tag));
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var url = "tag/" + $(".bookmark_bm_id").text();
        if(url == "undefiend" || url == "" || url == null)
        {
          console.log("Could not extract bm_id");
        } else {
          send_ajax("POST", {"tag": tag, "csrfmiddlewaretoken": csrftoken}, url)
        }
      });
    }
    
    input.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
          e.target.value.split(',').forEach(tag => {
            tags.push(tag);  
          });
          
          addTags();
          input.value = '';
        }
    });
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    document.addEventListener('click', (e) => {
      console.log(e.target.tagName);
      if (e.target.tagName === 'I') {
        const tagLabel = e.target.getAttribute('data-item');
        const index = tags.indexOf(tagLabel);
        var tag = e.target.parentNode
        tag.remove();
        
        var url = "tag/" + $(".bookmark_bm_id").text();
        send_ajax("DELETE", {"tag": tagLabel, "csrfmiddlewaretoken": csrftoken}, url);
        tags = [...tags.slice(0, index), ...tags.slice(index+1)];
        addTags();    
      }
    })
    
    input.focus();


  }
});
