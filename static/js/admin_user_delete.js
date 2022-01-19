document.addEventListener('click', (event) => {
    if (event.target.classList.contains('del_usr')) {
        event.preventDefault();
        let user_pk = event.target.dataset.pk;
        if (confirm('Вы уверены?')) {
            $.ajax({
                url: `user_delete/${user_pk}`,
                success: (data) => {
                    let row = event.target.parentElement.parentElement;
                    let status = row.querySelector('.is_active');
                    if (data.status === "True") {
                        row.classList.remove('not_active');
                        event.target.innerHTML = 'Удалить';
                    } else {
                        row.classList.add('not_active');
                        event.target.innerHTML = 'Восстановить';
                    };

                    status.innerHTML = `<span class="user_status">${data.status}</span>`;
                }
            });
        }
    }
});