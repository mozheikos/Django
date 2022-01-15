/*
1. Повесил обработчик на документ (можно было и на корзину, не суть в данном 
    случае)
2. Обрабатываю событие input, так как в нашем случае тег инпут позволяет как
изменять значение с помощью кнопок, так и вводить с клавиатуры, и, если пользователь
захочет ввести количество с клавиатуры - он кликнет в окошко, это будет клик и js
обработает событие, сделав AJAX-запрос. Но пользователь только щелкнул и еще
ничего не вводил, соответственно в метод edit полетит значение, которое и есть в базе.
С другой стороны, когда пользователь начнет вводить с клавиатуры - это не будет 
событие клик, и в базу ничего не отправится. Поэтому я решил обрабатывать именно
инпут.
3. От сервера возвращаю не рендер, а просто словарь JSON, из которого беру значения
переменных и подставляю в нужные элементы.
*/

document.addEventListener('input', (event) => {
    if (event.target.className === "value_edit") {
        let element = event.target;
        $.ajax({
            url: 'edit' + '/' + element.name + '/' + element.value,
            success: (data) => {
                let cost = element.parentElement.parentElement.querySelector('.row_cost');
                let total = document.querySelector('.total');
                let total_cost = document.querySelector('.total_cost');
                let menu_count = document.querySelector('.menu_count');
                let menu_cost = document.querySelector('.menu_cost');

                element.value = data.quantity;
                cost.innerHTML = `${data.product_cost} руб.`;
                total.innerHTML = `<b>Итого:</b> ${data.basket_count} шт.`;
                total_cost.innerHTML = `<b>Сумма:</b> ${data.basket_cost} рублей`;
                menu_count.innerHTML = `<b class="menu_basket_title">В корзине:</b> ${data.basket_count}
                товаров`;
                menu_cost.innerHTML = `<b class="menu_basket_title">На сумму:</b> ${data.basket_cost}
                рублей`;
            }
        });
        console.log('success');
    };
});