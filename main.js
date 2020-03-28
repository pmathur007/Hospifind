// typeform auth token: 5evke2jp3XoYUgdSuMgpVdKpovpweVBdPqTrZRiyB5To

$(document).ready(function() {
    const embedElement = document.getElementById("form_map");
    typeformEmbed.makeWidget(
        embedElement,
        'https://pranavmathur001.typeform.com/to/LO0U0p',
        {
            onSubmit: function() {

            }
        }
    );

    const typeform_url = 'https://api.typeform.com/forms/LO0U0p/responses'
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readystate == 4 && this.status == 200) {
            console.log(xhttp.responseText);
        }
    };

    xhttp.open("GET", typeform_url);
    xhttp.setRequestHeader("Authorization", "Bearer 5evke2jp3XoYUgdSuMgpVdKpovpweVBdPqTrZRiyB5To");
    xhttp.send(null);
});
