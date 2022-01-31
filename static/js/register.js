// let submit_btn = document.querySelector('#submit_registration')
// 
// submit_btn.addEventListener('click', (event) => {
//     event.preventDefault();
//     let form_data = document.querySelectorAll('INPUT');
//     let register_data = {}
//     form_data.forEach(el => {
//         if (el.tagName === "INPUT") {
//             register_data[el.name] = el.value;
//         }; // endif
//     }) // end forEach
// 
//     $.ajax({
//         async: true,
//         type: 'POST',
//         data: register_data,
//         url: ``,
//         success: (data) => {
//             let modal = document.querySelector('.modal_bg');
//             let text = document.querySelector('.modal_message');
//             let link = document.querySelector('.modal_link_ok');
//             modal.classList.add('show_reg');
//             text.innerText = data.status;
//             link.innerText = 'OK';
//             link.href = data.href;
//             console.dir(text);
//             console.dir(link);
//         }, //end success
//     }); // end ajax
// }) // end eventListener

// Все новые обработчики событий должны навешиваться после
// полной загрузки DOMа
$(document).ready(function () {

    // Навешиваем новый обработчик на кнопку
    $('[type="submit"]').click(function (event) {
        // Убираем стандартное событие
        event.preventDefault();

        // Выбираем форму и сериализуем
        //   https://api.jquery.com/serialize/
        var $form_serialized = $('form').serialize();

        // Отправляем форму асинхронно на сервер
        $.ajax({
            url: $('form').attr('action'),  // Забрали адрес отправки
            type: 'POST',
            data: $form_serialized,
            success: function (data) {
                console.log(data);
                let link = document.querySelector('.modal_link_ok');
                link.innerText = 'OK';
                link.href = data.href;
                // Вставляем текст из пришедшего сообщения
                $('.modal_message').text(data.status);
                // После заполнения показываем само окно
                $('.modal_bg').addClass("show_reg");
            },
        });
    });

});