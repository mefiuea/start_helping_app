window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');


    function show_id(event) {
        let ids = get_checked_checkboxes();
        let params = new URLSearchParams();
        ids.forEach(id => params.append("type_ids", id))
        let address = '/get_institutions_by_id?' + params.toString();
        fetch(address)
            .then(response => response.text())
            .then(data => document.getElementById("institutions").innerHTML = data);

    }

    function get_checked_checkboxes() {
        let markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
        let ids = [];
        markedCheckbox.forEach(box => ids.push(box.value));
        console.log(ids);
        return ids;
    }


    $(document).ready(function () {
        let li_buttons = $('.active');
        li_buttons.click(show_id);
    });

});
