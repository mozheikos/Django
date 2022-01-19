let search_button = document.querySelector('.find');
let search = document.querySelector('.find_user');
search_button.addEventListener('click', () => {
    let find_user = search.value;
    console.dir(search);
    if (find_user) {
        $.ajax({
            url: `${find_user}/`,
            success: (data) => {
                $('.users_list').html(data.result);
            }
        });
    };
});