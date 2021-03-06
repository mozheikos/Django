function getProductQuantity(row) {
    let product_quantity = Number.parseInt(row.querySelector('input[type="number"]').value);
    return product_quantity;
}

function getProductPrice(row) {
    let product_price = Number.parseFloat(row.querySelector('SPAN').innerText.replace(',', '.'));
    return product_price;
}

function setOrderTotal() {
    let order_total_quant = document.querySelector('.order_total_quantity');
    let order_total_cost = document.querySelector('.order_total_cost');

    let rows = document.querySelectorAll('.formset_row');
    let total_quant = 0;
    let total_cost = 0;

    for (let item of rows) {
        let _quant = getProductQuantity(item);
        total_quant += _quant;
        total_cost += getProductPrice(item) * _quant;
    };
    order_total_quant.innerText = total_quant.toString();
    order_total_cost.innerText = total_cost.toFixed(2).toString();

}

function addOrderItem() {
    let new_item = $('tr.formset_row').last()[0];
    let price = new_item.querySelector('SPAN');
    let select = new_item.querySelector('SELECT');
    let quant = new_item.querySelector('input[type="number"]');
    select.value = 0;
    price.innerText = 0;
    quant.value = 0;
    quant.disabled = true;
}

function deleteOrderItem(row) {
    let init_forms = Number.parseInt(document.querySelector('input[name="orderitems-INITIAL_FORMS"]').value);
    let row_number = Number.parseInt(row[0].querySelector('input[type="number"]').name.replace('orderitems-', '').replace('-quantity', ''));
    let total_forms = document.querySelector('input[name="orderitems-TOTAL_FORMS"]');
    // this check needed for correct work when deleting some form
    if (row_number < init_forms) {
        let _total_f = +total_forms.value;
        _total_f += 1;
        total_forms.value = _total_f;
    }
    // set orderitem quantity 0 for coorrect working total_order_information
    _val = row[0].querySelector('input[type="number"]');
    _val.value = 0;
    setOrderTotal();
}

window.addEventListener('load', () => {
    let order_form = document.querySelector('.order_table');
    if (order_form) {
        order_form.addEventListener('input', (event) => {
            if (event.target.type == "number") {
                setOrderTotal();
            }
            if (event.target.type == "select-one") {
                let pk = event.target.value;
                let row = event.target.parentElement.parentElement;
                let quant = row.querySelector('input[type="number"]');
                let price = row.querySelector('SPAN');
                if (pk != 0) {
                    quant.disabled = false;
                } else {
                    quant.disabled = true;
                }
                console.log(pk);
                $.ajax({
                    url: `/order/get_price/${pk}/`,
                    success: (data) => {
                        price.innerText = data.price;
                        setOrderTotal();
                    }
                });
            }
        });
    };

    $('.formset_row').formset({
        addText: '???????????????? ??????????????',
        deleteText: '??????????????',
        prefix: 'orderitems',
        added: addOrderItem,
        removed: deleteOrderItem
    });
});
