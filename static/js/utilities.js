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

async function getRequest(url, headers = {}) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw { status: response.status, data: errorData };
    }

    return await response.json(); // Return the original response as is
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error("Error parsing JSON response:", error);
    }
    throw error; // Ensure error is propagated as is
  }
}

async function postRequest(url, data, headers = {}) {
  try {
    let body;
    let isFormData = false;

    // Check if data is an instance of FormData (for file uploads)
    if (data instanceof FormData) {
      body = data;
      isFormData = true;
    } else {
      // Otherwise, assume JSON
      body = JSON.stringify(data);
      headers["Content-Type"] = "application/json"; // Set Content-Type for JSON
    }

    const response = await fetch(url, {
      method: "POST",
      headers: isFormData ? headers : { ...headers }, // Do not set Content-Type for FormData
      body,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw { status: response.status, data: errorData };
    }

    return await response.json(); // Return the original response as is
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error("Error parsing JSON response:", error);
    }
    throw error;
  }
}


async function putRequest(url, data, headers = {}) {
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw { status: response.status, data: errorData };
    }

    return await response.json(); // Return the original response as is
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error("Error parsing JSON response:", error);
    }
    throw error;
  }
}

async function deleteRequest(url, headers = {}) {
  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw { status: response.status, data: errorData };
    }

    return await response.json(); // Return the original response as is
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error("Error parsing JSON response:", error);
    }
    throw error;
  }
}

async function dispatchRequest(key, method, url, data = null, persist = true, fallback = true) {
  const accessToken = TokenStore?.getAccessToken();

  let headers = {};
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  try {
    let response;

    switch (method.toUpperCase()) {
      case "GET":
        response = await getRequest(url, headers);
        break;
      case "POST":
        response = await postRequest(url, data, headers);
        break;
      case "PUT":
        response = await putRequest(url, data, headers);
        break;
      case "DELETE":
        response = await deleteRequest(url, headers);
        break;
      default:
        throw new Error(`Unsupported HTTP method: ${method}`);
    }

    // Persist successful response if needed
    if (persist && key) {
      DataStore.set(key, response);
    }

    return response; // Return the original response as is
  } catch (error) {
    console.error(`Request failed for key "${key}":`, error);

    // Fallback to old data if enabled
    if (fallback && key) {
      const oldData = DataStore.get(key);
      if (oldData) {
        console.warn(`Using old data for key "${key}" due to request failure.`);
        return oldData;
      }
    }

    throw error; // Re-throw the error for further handling
  }
}


function formatTime(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diffInMinutes = Math.floor((now - date) / (1000 * 60));

  if (diffInMinutes < 60) {
      return `${diffInMinutes} mins ago`;
  } else if (diffInMinutes < 1440) { // Less than 24 hours
      return `${Math.floor(diffInMinutes / 60)} hour${Math.floor(diffInMinutes / 60) > 1 ? 's' : ''} ago`;
  } else {
      return `${Math.floor(diffInMinutes / 1440)} day${Math.floor(diffInMinutes / 1440) > 1 ? 's' : ''} ago`;
  }
}


