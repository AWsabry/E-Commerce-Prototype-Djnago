$.ajax({
    type: "GET",
    url: "/words_search_ajax/",
    data: {'input':search_input.value},
    beforeSend: function(){
        dropdownMenu.innerHTML = preloadSearchAjax;
    },
    success: function (response) {
        dropdownMenu.innerHTML = '';
        var output = JSON.parse(response);
        if(output.word.length || output.user.length){
                if(output.word.length){
                    for (let j = 0; j < output.word.length; j++) {
                        const element = output.word[j][0];
                        dropdownMenu.insertAdjacentHTML('beforeend', `<li><button type="submit" class="no-sidebar-search" name="words_search" value="${element}"><i class="fas fa-chevron-left drop-icon" aria-hidden="true"></i><span>${element}</span></button></li>`)
                    }
                }
                
                if(output.user && output.user.length){
                    for (let j = 0; j < output.user.length; j++) {
                        const element = output.user[j][0];
                        dropdownMenu.insertAdjacentHTML('beforeend', `<li><button type="submit" class="no-sidebar-search" name="words_search" value="${element}"><i class="fas fa-user-tie drop-icon" aria-hidden="true"></i><span>${element}</span></button></li>`)
                    }
                }
        }else{
                $('.dropdownContainer').removeClass('search-input-show');
        }
    }, error: function(response){
    }
});