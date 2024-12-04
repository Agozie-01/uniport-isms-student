 
// Define validation constraints
const loginConstrants = {
    username: {
        presence: {allowEmpty: false, message: "is required"},
    },
    password: {
      presence: {allowEmpty: false, message: "is required." },
    }
};


 // Handle form submission
 document.getElementById("login-form").onsubmit = async function(event) {
    event.preventDefault(); // Prevent default form submission (page reload)
    
    clearErrors(); //Clear old errors

    // Retrieve form data
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get("username"),
        password: formData.get("password"),
    };

    // Call validation function
    const result = validateForm(loginData, loginConstrants);

    // Display errors if validation fails
    if (result) {
        displayErrors(result);
        return; // Prevent form submission if validation fails
    }

    // Show the loader when the login button is clicked
    showLoader("login-loader");
    disableForm(this.id);
    
    try {
        const response = await fetch('/api/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginData)
        });
      
        if (!response.ok) {
          const errorData = await response.json();
          toastError("Invalid login credentials");
          hideLoader("login-loader");
          enableForm(this.id);
        } else {
          const data = await response.json();

          TokenStore.set(data?.access, data?.refresh);
         
          toastSuccess("Logged in successfully!", "right", function() {
            window.location.href = '/dashboard';
          })
        }
      } catch (error) {
        hideLoader("login-loader");
        toastError("Login error. Please try again later.");
        enableForm(this.id);
      }
      
};