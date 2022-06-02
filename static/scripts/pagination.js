window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    let actual_page_foundations = 0
    let actual_page_organizations = 0
    let actual_page_local_collections = 0
    console.log('actual page foundations = ' + actual_page_foundations)
    console.log('actual page organizations = ' + actual_page_organizations)
    console.log('actual page local collections = ' + actual_page_local_collections)

    // institutions pagination
    function get_foundations() {
        console.log('actual page foundations = ' + actual_page_foundations)
        let params = new URLSearchParams();
        params.append("page", actual_page_foundations)
        let address = 'get_foundations_by_page/?' + params.toString();
        let zmienna = fetch(address).then(function (response) {
            return response.text();
        }).then(function (data) {
            console.log(data)
            console.log(document.getElementById('ins-pag').innerHTML)
            return document.getElementById('ins-pag').innerHTML = data;
        })
    }


    function prev_foundations() {
        if (actual_page_foundations > 0) {
            actual_page_foundations -= 1
        }
        get_foundations()
    }

    function next_foundations() {
        actual_page_foundations += 1
        get_foundations()
    }

    // organizations pagination
    function get_organizations() {
        console.log('actual page = ' + actual_page_organizations)
        let params = new URLSearchParams();
        params.append("page", actual_page_organizations)
        let address = 'get_organizations_by_page/?' + params.toString();
        let zmienna = fetch(address).then(function (response) {
            return response.text();
        }).then(function (data) {
            console.log(data)
            console.log(document.getElementById('org-pag').innerHTML)
            return document.getElementById('org-pag').innerHTML = data;
        })
    }


    function prev_organizations() {
        if (actual_page_organizations > 0) {
            actual_page_organizations -= 1
        }
        get_organizations()
    }

    function next_organizations() {
        actual_page_organizations += 1
        get_organizations()
    }

    // local collections pagination
    function get_local_collections() {
        console.log('actual page = ' + actual_page_local_collections)
        let params = new URLSearchParams();
        params.append("page", actual_page_local_collections)
        let address = 'get_local_collections_by_page/?' + params.toString();
        let zmienna = fetch(address).then(function (response) {
            return response.text();
        }).then(function (data) {
            console.log(data)
            console.log(document.getElementById('loc-pag').innerHTML)
            return document.getElementById('loc-pag').innerHTML = data;
        })
    }


    function prev_local_collections() {
        if (actual_page_local_collections > 0) {
            actual_page_local_collections -= 1
        }
        get_local_collections()
    }

    function next_local_collections() {
        actual_page_local_collections += 1
        get_local_collections()
    }


    $(document).ready(function () {
        // institutions
        let pag_prev_s1 = $('#pag-prev-s1');
        pag_prev_s1.click(prev_foundations);
        let pag_next_s1 = $('#pag-next-s1');
        pag_next_s1.click(next_foundations);
        // organizations
        let pag_prev_s2 = $('#pag-prev-s2');
        pag_prev_s2.click(prev_organizations);
        let pag_next_s2 = $('#pag-next-s2');
        pag_next_s2.click(next_organizations);
        // local collections
        let pag_prev_s3 = $('#pag-prev-s3');
        pag_prev_s3.click(prev_local_collections);
        let pag_next_s3 = $('#pag-next-s3');
        pag_next_s3.click(next_local_collections);
    });

});
