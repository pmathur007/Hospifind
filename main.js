var currentPage = 0;

$(function() {
    var hospitalId = -1;

    showPage(0); // first load the patient/hospital selection
    $('#patient_button').on('click', function() {
        currentPage = 1; // go to the patient form
        showPage();
    });

    $('#hospital_button').on('click', function() {
        currentPage = 2; // go to the hospital form
        showPage();
    });

    $('#prev_button').on('click', function() {
        if (currentPage === 2)
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
            var patientName = $("#patient_name").val();
            var patientAge = $("#age").val();
            var patientAddress = $("#address").val();
            var transportation = $("input[name='transportation']:checked").val();

            if (patientName === "" || patientAge === "" || patientAddress === "" || transportation === "")
            {
                alert("Please fill out all fields")
            }
            else
            {
                if (transportation === "walking")
                    transportation = 0;
                else if (transportation === "bicycling")
                    transportation = 1;
                else if (transportation === "driving")
                    transportation = 2;
                else
                    transportation = 3;
                    
                console.log(transportation);
                var weights = [0.879, 0.677, 0.381, 0.334, 0.186, 0.139, 0.114, 0.05, 0.048, 0.037]
                var symptomsFields = $("input[name='is_corona']");
                var symptoms = 0;
                for (let i = 0; i < weights.length; i++)
                {
                    symptoms += symptomsFields[i].checked ? weights[i] : 0;
                }
                symptoms = (symptoms / 2.845) * 10;

                var prevCondFields = $("input[name='pre_conditions']");
                var prev_conditions = 0;
                for (let i = 0; i < prevCondFields.length; i++)
                {
                    prev_conditions += prevCondFields[i].checked ? 1 : 0;
                }

                patientData = {
                    "age": patientAge,
                    "symptoms": symptoms,
                    "prev_conditions": prev_conditions
                };
            }
        }
        else if (currentPage === 2)
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
        else if (currentPage == 3)
        {
            var capacity = $("#capacity").val();
            var beds = $("#beds").val();
            var icus = $("#icu").val();
            var ventilators = $("#ventilators").val()
            var tests = $("#tests").val();
            var covidPatients = $("#covid_patients").val();

            if (capacity === "" || beds === "" || icus === "" || ventilators === "" || tests === "" || covidPatients === "")
            {
                alert("Please fill out all fields");
            }
            else
            {
                hospitalData = {
                    "hospital_id": hospitalId,
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

    if (currentPage % 2 === 1)
    {
        $('#next_button').text('Submit');
    }
    else
    {
        $('#next_button').text('Next');
    }
}
