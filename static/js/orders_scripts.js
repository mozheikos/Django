window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = Number.parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = Number.parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = Number.parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = Number.parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = Number.parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        } //end if
    } //end for

    if (!order_total_quantity) {
        for (let i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        } //end for
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }//end if

    /*$('.order_form').on('change', 'input[type="number"]', function () {
        let target = event.target;
        orderitem_num = Number.parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = Number.parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        } //end if
    });*/ // end order_form event listener quantity*/

    document.addEventListener('input', (event) => {
        if (event.target.type == "number") {
            let target = event.target;
            // Добавил проверку target.value, иначе джанго не удаляет строку из заказа, а просто ставит количество = 0
            let _delete = target.parentElement.parentElement.querySelector('INPUT[type="checkbox"]');
            if (target.value == 0) {
                _delete.checked = true;
            } else {
                _delete.checked = false;
            }

            orderitem_num = Number.parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
            if (price_arr[orderitem_num]) {
                orderitem_quantity = Number.parseInt(target.value);
                delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
                orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            } //end if
        }

    });

    $('.order_form').on('click', 'input[type="checkbox"]', function () {
        let target = event.target;
        orderitem_num = Number.parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        } //end if
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }); // end event listener delete



    /*function deleteOrderItem(row) {
        let target_name = row.querySelector('input[type="number"]').name;
        orderitem_num = Number.parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    } // end delete func

    $('.order_form select').change(function () {
        var target = event.target;
        console.log(target);
    });*/

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    } //end render func


    /* Код я написал, но Бибилиотеку я отключил. Некорректно себя ведет:
    1. При добавлении строки в форму она копирует предыдущую, цена не правильная, в общем криво
    2. Удаление фактически не работает, так как сама библиотека при нажатии на кнопку просто
    скрывает строку, в джанго не приходит инфа об удалении. Знаю как поправить, но это в код
    библиотеки надо лезть, не стал
    3. Реально нормально работает только на изменение количества

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });*/
}; //end onload func