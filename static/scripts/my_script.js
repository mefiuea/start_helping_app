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
        // get tex from checked checkboxes
        let markedCheckbox = document.querySelectorAll('input[name="categories"]:checked');
        let category_names_list = []
        for (let i = 0; i < markedCheckbox.length; i++) {
            category_names_list.push(markedCheckbox[i].nextElementSibling.nextElementSibling.innerText);
        }
        console.log(category_names_list)

        let bags_quantity = document.getElementById('bags').value;
        let institution_name = document.querySelector('input[name="organization"]:checked').nextElementSibling.nextElementSibling.children[0].innerText;
        let street_name = document.getElementById('street').value;
        let city_name = document.getElementById('city').value;
        let postal_code = document.getElementById('postal-code').value
        let phone_number = document.getElementById('phone-number').value
        let pickup_date = document.getElementById('pickup-date').value
        let pickup_time = document.getElementById('pickup-time').value
        let comments_for_courier = document.getElementById('comments-for-courier').value

        console.log(bags_quantity, institution_name, street_name, city_name, postal_code, phone_number, pickup_date,
            pickup_time, comments_for_courier)

        let bag_word = ''
        if (bags_quantity === '1') {
            bag_word = ' worek: '
        } else {
            bag_word = ' worków: '
        }
        let sum = bags_quantity + bag_word
        for (let i = 0; i < category_names_list.length; i++) {
            sum += category_names_list[i] + ' ';
        }
        document.getElementById('bags-summary').children[1].innerText = sum
        document.getElementById('institution-summary').children[1].innerText = 'Dla: ' + institution_name
        document.getElementById('street-summary').innerText = street_name
        document.getElementById('city-summary').innerText = city_name
        document.getElementById('postal-code-summary').innerText = postal_code
        document.getElementById('phone-number-summary').innerText = phone_number
        document.getElementById('pickup-date-summary').innerText = pickup_date
        document.getElementById('pickup-time-summary').innerText = pickup_time
        document.getElementById('comments-for-courier-summary').innerText = comments_for_courier

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