// Все новые обработчики событий должны навешиваться после
// полной загрузки DOMа
$(document).ready(function () {

    // Навешиваем новый обработчик на кнопку
    let form = document.querySelector('FORM');
    form.addEventListener('click', (event) => {
        if (event.target.type == 'submit') {

            // Убираем стандартное событие
            event.preventDefault();

            // Выбираем форму и сериализуем
            //   https://api.jquery.com/serialize/
            var $form_serialized = $('form').serialize();
            let btn = event.target;
            let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');

            // Отправляем форму асинхронно на сервер
            $.ajax({
                url: form.action,
                type: 'POST',
                data: $form_serialized,
                success: function (data) {

                    let link = document.querySelector('.modal_link_ok');
                    link.innerText = 'OK';

                    if (!data.errors) {

                        link.href = data.href;
                        // Вставляем текст из пришедшего сообщения
                        let msg = document.querySelector('.modal_message');
                        msg.innerText = data.status;
                        // После заполнения показываем само окно
                        let modal = document.querySelector('.modal_bg');
                        modal.classList.add('show_reg');

                    } else {

                        form.innerHTML = data.form;
                        form.prepend(csrf);
                        form.append(btn);
                        $('.errorlist').addClass('red');

                    };
                },
            });
        }
    });

});