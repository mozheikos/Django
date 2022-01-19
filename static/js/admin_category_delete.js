document.addEventListener('click', (event) => {
    if (event.target.classList.contains('del_cat')) {
        event.preventDefault();
        let category_pk = event.target.dataset.pk;
        if (confirm('Вы уверены?')) {
            $.ajax({
                url: `category_delete/${category_pk}`,
                success: (data) => {
                    let row = event.target.parentElement.parentElement;

                    if (data.status === "True") {
                        row.classList.remove('not_active');
                        event.target.innerHTML = 'Удалить';
                    } else {
                        row.classList.add('not_active');
                        event.target.innerHTML = 'Восстановить';
                    };
                }
            });
        }
    }
});