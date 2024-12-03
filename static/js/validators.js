 /**
     * Function to validate the form.
     * @param {Object} formData - Form data to validate.
     * @param {Object} constraints - Form constrants.
     */
 function validateForm(formData, constraints) {
    // Run validation using Validate.js
    var validationResult = validate(formData, constraints);
    return validationResult;
  }

  /**
   * Display errors dynamically by looping through the error object.
   * @param {Object} errors - Errors object containing field names and error messages.
   */
 // Function to display error messages
function displayErrors(errors) {
    // Clear previous error messages
    document.querySelectorAll(".error").forEach((el) => (el.textContent = ""));
  
    // Loop through the errors and display them
    for (const [field, messages] of Object.entries(errors)) {
      const errorElement = document.getElementById(`${field}-error`);

      if (errorElement && Array.isArray(messages)) {
        // Join multiple error messages and display
        errorElement.textContent = messages.join(", ");
      }
    }
  }

