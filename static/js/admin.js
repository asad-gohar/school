$(document).ready(function() {
    $('.sideMenuToggler').on('click', function() {
        $('.wrapper').toggleClass('active');
    });

    var adjustSidebar = function() {
        $('.sidebar').slimScroll({

            height: document.documentElement.clientHeight - $('.navbar').outerHeight()

        });
    };

    adjustSidebar();
    $(window).resize(function() {
        adjustSidebar();
    });

});

(function($) {
    "use strict";


    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input100').each(function() {
        $(this).on('blur', function() {
            if ($(this).val().trim() != "") {
                $(this).addClass('has-val');
            } else {
                $(this).removeClass('has-val');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit', function() {
        var check = true;

        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function() {
        $(this).focus(function() {
            hideValidate(this);
        });
    });

    function validate(input) {
        if ($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        } else {
            if ($(input).val().trim() == '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }


})(jQuery);



var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    //... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    //... and run a function that will display the corr  document.getElementById("myAnchor").focus();ect step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {

    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // currentTab.getElementById("myAnchor").focus();
    // if you have reached the end of the form...
    if (currentTab >= x.length) {
        // ... the form gets submitted:
        document.getElementById("regForm").submit();
        return false;
    }

    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, z, i, valid = true;

    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");

    z = document.getElementById("textarea");

    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:

            document.getElementsByClassName("error")[currentTab].innerHTML = "* please fill them all";
            y[i].className += " invalid";
            y[i].focus();

            // and set the current valid status to false
            valid = false;
            return valid;
        }


    }

    if (valid == true) {
        document.getElementsByClassName("error")[currentTab].innerHTML = "";
    }

    if (currentTab == 1) {

        if (z.value == "") {
            if (f == true) {
                document.getElementById("language").innerHTML = "";
            }
            // add an "invalid" class to the field:
            document.getElementsByClassName("error")[currentTab].innerHTML = "* please fill them all";
            z.className += "invalid";
            // and set the current valid status to false
            z.focus();
            valid = false;
            return valid;
        }
        var language = document.getElementsByClassName("language");
        var f = true;

        if (valid == true && f == true) {
            document.getElementById("button_control").style.display = "none";
            document.getElementsByClassName("loader")[0].style.display = "block";
        }
        return f, valid;
        for (let index = 0; index < language.length; index++) {

            if (language[index].checked == true) {
                document.getElementById("language").innerHTML = "";


                f = true;


            } else {
                f = false;

            }


        }
        if (valid == true) {

            document.getElementById("language").innerHTML = "* please Select At least one";

            return f;

            // if (currentTab == 2) {


            // }

        }


    }



    // If the valid status is true, mark the step as finished and valid:
    if (valid) {

        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace("active", "");
    }
    //... and adds the "active" class on the current step:
    x[n].className += " active";
}




$(function() {
    $("#datepicker").datepicker();
});