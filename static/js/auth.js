 
 
 // Handle form submission
 document.getElementById("login-form").onsubmit = async function(event) {
    event.preventDefault(); // Prevent default form submission (page reload)

    // Retrieve form data
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get("username"),
        password: formData.get("password"),
    };

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
        } else {
          const data = await response.json();
         
          toastSuccess("Logged in successfully!", "right", function() {
            window.location.href = '/dashboard/';
          })
        }
      } catch (error) {
        console.log(error);
        Swal.fire({
          title: 'Error',
          text: 'Unable to connect to the server',
          icon: 'error',
          confirmButtonText: 'Retry'
        });
      }
      
};