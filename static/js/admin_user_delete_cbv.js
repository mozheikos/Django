document.addEventListener('click', (event) => {
    if (event.target.classList.contains('del_usr')) {
        event.preventDefault();
        let form = event.target.parentElement.querySelector('form');
        form.classList.add('show');
    };//end 1st if

    if (event.target.classList.contains('confirm')) {
        event.preventDefault();
        let form = event.target.parentElement;
        let form_data = form.querySelectorAll('[type=hidden]');
        let user_data = {};
        form_data.forEach(el => {
            user_data[el.name] = el.value
        }); // end forEach
        $.ajax({
            async: true,
            type: 'POST',
            data: user_data,
            url: `user_delete/${user_data.pk}/`,
            //dataType: form.enctype,
            success: (data) => {
                let row = event.target.parentElement.parentElement.parentElement;
                let status = row.querySelector('.is_active');
                let del_btn = row.querySelector('.del_usr');
                let confirm_btn = row.querySelector('.confirm');
                console.log(row, status);
                if (data.status === "True") {
                    row.classList.remove('not_active');
                    del_btn.innerHTML = 'Удалить';
                    confirm_btn.value = 'Удалить';
                } else {
                    row.classList.add('not_active');
                    del_btn.innerHTML = 'Восстановить';
                    confirm_btn.value = 'Восстановить';
                };
                status.innerHTML = data.status;
                console.log('success');

            }//success func end
        });// ajax end
        form.classList.remove('show');

    } else if (event.target.classList.contains('cancel')) {
        event.preventDefault();
        let form = event.target.parentElement;
        console.log('canceled');
        form.classList.remove('show');
    } // end 2nd if

}); //end document.eventListener