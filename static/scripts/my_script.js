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
            console.log(data)
            // console.log(document.getElementById('ins').innerHTML)
            return document.getElementById('ins').innerHTML = data
        })
    }

    function get_checked_checkboxes() {
        let markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
        let ids = [];
        markedCheckbox.forEach(box => ids.push(box.value));
        console.log(ids);
        return ids;
    }


    $(document).ready(function () {
        let li_buttons = $('.checkboxy');
        li_buttons.click(show_id);
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