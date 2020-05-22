function validateRadio(fieldName) {
    radios = document.getElementsByName(fieldName);
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked)
            return true;
    }
    return false;
}

function getFieldValues(fieldName) {
    inputs = document.getElementsByName(fieldName);
    selected = [];
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].checked)
            selected.push(inputs[i].value)
    }
    if (selected.length === 1)
        return selected[0];
    return selected;
}

function validatePatientForm() {
    let invalidSections = [];

    if (!validateRadio("emergency")) {
        formValid = false;
        invalidSections.push("Whether you are in a serious/life threatening condition");
    }
    if (!validateRadio("age")) {
        formValid = false;
        invalidSections.push("Your age");
    }
    if (!validateRadio("near_covid")) {
        formValid = false;
        invalidSections.push("Whether you have been in an area where COVID 19 is widespread");
    }

    if (invalidSections.length > 0) {
        alert("Please indicate\n" + invalidSections.concat());
    } else {
        formData = {
            "emergency": getFieldValues("emergency"),
            "age": getFieldValues("age"),
            "symptoms": getFieldValues("symptoms"),
            "conditions": getFieldValues("conditions"),
            "near_covid": getFieldValues("near_covid")
        };

        $.ajax({
            type: "POST",
            url: "/patient_form",
            contentType: "application/json",
            data: JSON.stringify(formData)
        }).done(function(data) {
            document.write(data);
        });
    }
}