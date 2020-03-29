currentPage = 0;

$(function() {
    showPage(0); // first load the patient/hospital selection
    $('#patient_button').on('click', function() {
        currentPage = 1; // go to the patient form
        showPage();
    });

    $('#hospital_button').on('click', function() {
        currentPage = 3; // go to the hospital form
        showPage();
    });

    $('#prev_button').on('click', function() {
        if (currentPage === 3)
        {
            currentPage = 0
        }
        else
        {
            currentPage = currentPage - 1;
        }
        showPage();
    });

    // validate form before you move on to the next page
    $('#next_button').on('click', function() {
        if (currentPage === 1)
        {
            patientName = $("#patient_name").val();
            patientAge = $("#age").val();
            patientAddress = $("#address").val();
            transportation = $("input[name='transportation']:checked").val();

            if (patientName == "" || patientAge == "" || patientAddress == "" || transportation == undefined)
            {
                console.log("invalid");
            }
            else
            {
                currentPage = currentPage + 1;
                showPage();
            }
        }
        else if (currentPage === 2)
        {
            patientName = $("#patient_name").val();
            patientAge = $("#age").val();
            patientAddress = $("#address").val();
            transportation = $("input[name='transportation']:checked").val();

            let weights = [0.879, 0.677, 0.381, 0.334, 0.186, 0.139, 0.114, 0.05, 0.048, 0.037]
            symptomsFields = $("input[name='is_corona']");
            symptoms = 0;
            for (let i = 0; i < weights.length; i++)
            {
                symptoms += symptomsFields[i].checked ? weights[i] : 0;
            }
            symptoms = (symptoms / 2.845) * 10;

            prevCondFields = $("input[name='pre_conditions']");
            prev_conditions = 0;
            for (let i = 0; i < prevCondFields.length; i++)
            {
                prev_conditions += prevCondFields[i].checked ? 1 : 0;
            }

            patientData = {
                "age": patientAge,
                "transporation": transporation,
                "symptoms": symptoms,
                "prev_conditions": prev_conditions
            };

        }
        else if (currentPage === 3)
        {
            hospitalId = $("#hospital_id").val();
            const toSend =
            {
                "hospital_id": hospitalId
            };

            $.post("https://wb4tf07f30.execute-api.us-east-1.amazonaws.com/prod/validate-hospital", JSON.stringify(toSend), function(data, status) {
                if (status === "success")
                {
                    if (data["body"] === "\"Found\"")
                    {
                        currentPage++;
                        showPage();
                    }
                    else
                    {
                        alert("Hospital ID invalid")
                    }
                }
            });
        }
        else if (currentPage == 4)
        {
            hospital_id = $("hospital_id").val();
            capacity = $("#capacity").val();
            beds = $("#beds").val();
            icus = $("#icu").val();
            ventilators = $("#ventilators").val()
            tests = $("#tests").val();
            covidPatients = $("#covid_patients").val();

            hospitalData = {
                "hospital_id": hospital_id,
                "capacity": capacity,
                "beds": beds,
                "icus": icus,
                "ventilators": ventilators,
                "tests": tests,
                "covid_patients": covidPatients
            };

            $.post("https://wb4tf07f30.execute-api.us-east-1.amazonaws.com/prod/update", JSON.stringify(hospitalData), function(data, status) {
                if (status === "success")
                {
                    alert("Thanks for submitting! Your data helps raise the hospital capacity line accross the country");
                }
            });
        }
        else
        {
            currentPage++;
            showPage();
        }
    })
});

function showPage()
{
    formPages = $('.form_page');
    for (let i = 0; i < formPages.length; i++)
    {
        if (i === currentPage)
        {
            $(formPages[i]).css('display', 'block');
        }
        else
        {
            $(formPages[i]).css('display', 'none');
        }
    }

    if (currentPage === 0)
    {
        $('.next_prev').css('display', 'none');
    }
    else
    {
        $('.next_prev').css('display', 'inline-block');
    }

    if (currentPage % 2 === 0)
    {
        $('#next_button').text('Submit');
    }
    else
    {
        $('#next_button').text('Next');
    }
}
