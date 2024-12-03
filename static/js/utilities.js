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

function clearErrors() {
   // Clear previous error messages
   document.querySelectorAll(".error").forEach((el) => (el.textContent = ""));
}

// Initialize a spinner (loader) instance
let loader = new Spinner({
  lines: 12,            // Number of lines
  length: 7,            // Length of each line
  width: 5,             // Line thickness
  radius: 10,           // Radius of the inner circle
  scale: 1,             // Scale of the spinner
  corners: 1,           // Roundness of the corners
  color: '#000',        // Color of the spinner
  opacity: 0.25,        // Opacity of the spinner
  rotate: 0,            // Rotation of the spinner
  direction: 1,         // 1: clockwise, -1: counterclockwise
  speed: 1,             // Speed of the spinner
  trail: 60,            // How much of the trail to show
  shadow: false,        // Whether or not to cast a shadow
  hwaccel: false,       // Whether to use hardware acceleration
  className: 'spinner', // CSS class to apply to the spinner
  zIndex: 2e9,          // z-index of the spinner
  top: '50%',           // Top position relative to the container
  left: '50%'           // Left position relative to the container
});

// Function to show the loader when the form is submitted
function showLoader(elem) {
  const loaderElement = document.getElementById(elem);
  loaderElement.style.display = 'block'; // Show the loader
  loader.spin(loaderElement);           // Start the spinner
}

// Function to hide the loader after form submission
function hideLoader(elem) {
  const loaderElement = document.getElementById(elem);
  loaderElement.style.display = 'none'; // Hide the loader
  loader.stop();                        // Stop the spinner
}

// Function to disable all form inputs and buttons
function disableForm(formId) {
  const form = document.getElementById(formId);
  Array.from(form.elements).forEach((element) => {
    element.disabled = true;
  });
}

// Function to re-enable all form inputs and buttons
function enableForm(formId) {
  const form = document.getElementById(formId);
  Array.from(form.elements).forEach((element) => {
    element.disabled = false;
  });
}
