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
        if (currentPage === 2)
        {
            patientSubmit();
        }
        else if (currentPage == 4)
        {
            hospitalSubmit();
        }
        else
        {
            currentPage = currentPage + 1;
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
