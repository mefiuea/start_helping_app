window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');


    function show_id() {
        let ids = get_checked_checkboxes();
        let params = new URLSearchParams();
        ids.forEach(id => params.append("type_ids", id))
        let address = '/get_institutions_by_id/?' + params.toString();
        let zmienna = fetch(address).then(function (response) {
            return response.text();
        }).then(function (data) {
            // console.log(data)
            // console.log(document.getElementById('ins').innerHTML)
            return document.getElementById('ins').innerHTML = data;
        })
    }

    function get_checked_checkboxes() {
        let markedCheckbox = document.querySelectorAll('input[name="categories"]:checked');
        let ids = [];
        markedCheckbox.forEach(box => ids.push(box.value));
        console.log(ids);
        return ids;
    }

    function form_summary() {
        let bags_quantity = document.getElementById('bags').value;
        let institution_name = document.querySelector('input[name="organization"]:checked').value;
        let street_name = document.getElementById('street').value;
        let city_name = document.getElementById('city').value;
        let postal_code = document.getElementById('postal-code').value
        let phone_number = document.getElementById('phone-number').value
        let pickup_date = document.getElementById('pickup-date').value
        let pickup_time = document.getElementById('pickup-time').value
        let comments_for_courier = document.getElementById('comments-for-courier').value

        console.log(bags_quantity, institution_name, street_name, city_name, postal_code, phone_number, pickup_date,
            pickup_time, comments_for_courier)
    }


    $(document).ready(function () {
        let checkbox_buttons = $('.checkboxy');
        checkbox_buttons.click(show_id);
        let next_button = $('#summary-button');
        // let next_button = $('.next-step');
        next_button.click(form_summary);
    });
    
    // const checkButton = document.getElementById('cb');
    // checkButton.addEventListener('click', function () {
    // if (this.checked) {
    //     console.log('nacisniete')
    // } else {
    //     let markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
    //     let ids = [];
    //     markedCheckbox.forEach(box => ids.push(box.value));
    //     console.log(ids);
    // }
});

    // });