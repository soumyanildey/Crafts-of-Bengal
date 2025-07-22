function check()
{
    let fname = document.forms["signup"]["fname"].value;
    let lname = document.forms["signup"]["lname"].value;
    let mail = document.forms["signup"]["email"].value;
    let pw = document.forms["signup"]["pw"].value;
    let cpw = document.forms["signup"]["cpw"].value;
    let ph = document.forms["signup"]["cno"].value;
    let gen = document.forms["signup"]["gender"].value;

                if((fname==null||fname==""))
                {
                    alert("First Name field must not be empty");
                    document.forms["signup"]["fname"].focus();
                    return false;
                }
                if((lname==null||lname==""))
                {
                    alert("Last Name field must not be empty");
                    document.forms["signup"]["lname"].focus();
                    return false;
                }
                if((mail==null||mail==""))
                {
                    alert("Email id field must not be empty");
                    document.forms["signup"]["email"].focus();
                    return false;
                }
                else
                {
                    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                    if(!mail.match(mailformat))
                    {
                        alert("Email id is invalid");
                        document.forms["signup"]["email"].focus();
                        return false;
                    }
                }
                if(ph===""|| isNaN(ph)==true || ph<1000000000 || ph>9999999999 )
                {
                    alert("Enter a valid Contact No.");
                    document.forms["signup"]["cno"].focus();
                    return false;
                }
                if((gen==null||gen==""))
                {
                    alert("Gender field must not be empty");
                    return false;
                }
                if((pw==null||pw==""))
                {
                    alert("Password field must not be empty");
                    document.forms["signup"]["pw"].focus();
                    return false;
                }
                if(pw.length<6)
                {
                    alert("Password must be minimum 6 characters");
                    document.forms["signup"]["pw"].value="";
                    document.forms["signup"]["pw"].focus();
                    return false;
                }
                if((cpw==null||cpw==""))
                {
                    alert("Confirm Password field must not be empty");
                    document.forms["signup"]["cpw"].focus();
                    return false;
                }
                if(pw!=cpw)
                {
                    alert("Password do not match");
		            document.forms["signup"]["cpw"].value="";
		            document.forms["signup"]["cpw"].focus();
		            return false;
                }


}

function checkn()
{
    let mail = document.forms["login"]["email"].value;
    let pw = document.forms["login"]["pw"].value;
            if((mail==null||mail==""))
                {
                    alert("Email id field must not be empty");
                    document.forms["login"]["email"].focus();
                    return false;
                }
            if((pw==null||pw==""))
                {
                    alert("Password field must not be empty");
                    document.forms["login"]["pw"].focus();
                    return false;
                }
}
// Ensure DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get the elements
    const passwordInput = document.getElementById("pass-word");
    const togglePassword = document.getElementById("toggle-password");

    // Add event listener to the toggle icon
    togglePassword.addEventListener("click", () => {
        // Toggle the input type
        const isPassword = passwordInput.type === "password";
        passwordInput.type = isPassword ? "text" : "password";

        // Toggle the icon classes
        if (isPassword) {
            togglePassword.classList.remove("fa-eye");
            togglePassword.classList.add("fa-eye-slash");
        } else {
            togglePassword.classList.remove("fa-eye-slash");
            togglePassword.classList.add("fa-eye");
        }
    });
});
