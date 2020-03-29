currentPage = 0;

$(function() {
    showPage(0);
    $('#patient_button').on('click', function() {
        currentPage = 1;
        showPage();
    });

    $('#hospital_button').on('click', function() {
        currentPage = 3;
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

            }
        }
        else if (currentPage === 2)
        {
            patientSubmit();
        }
        else if (currentPage === 3)
        {
            hospitalId = $("#hospital_id").val();
            const toSend =
            {
                hospital_id: hospitalId
            };

            xhr = new XMLHttpRequest();
            xhr.onload = function() {
                if (xhr.status === 200)
                {
                    console.log("FUCK YEAH");
                }
            };

            xhr.open("POST", "https://wb4tf07f30.execute-api.us-east-1.amazonaws.com/prod");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify(toSend));
        }
        else if (currentPage == 4)
        {
            capacity = $("#capacity").val();
            beds = $("#beds").val();
            icus = $("#icu").val();
            ventilators = $("#ventilators").val()
            tests = $("#tests").val();
            covidPatients = $("#covid_patients").val();

            hospitalSubmit();
        }
        else
        {
            currentPage = currentPage + 1;
            showPage();
        }
    })
});

function patientSubmit()
{

}

function hospitalSubmit()
{

}

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
