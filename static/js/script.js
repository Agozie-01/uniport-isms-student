window.dashboardStats = function dashboardStats() {
  return {
    stats: [
      { title: 'Total Students', value: 0, icon: 'bi-people' },
      { title: 'Total Courses', value: 0, icon: 'bi-journal-bookmark' },
      { title: 'Average Grade', value: "N/A", icon: 'bi-star' },
      { title: 'Results Uploaded', value: 0, icon: 'bi-clock-history' }
    ],

    // Fetch stats and update
    async fetchStats() {
      try {
        const dashboardStats = await dispatchRequest("dashboardStats", "GET", "/api/dashboard/stats");

        this.stats = [
          { title: 'Total Students', value: dashboardStats.total_students, icon: 'bi-people' },
          { title: 'Total Courses', value: dashboardStats.total_courses, icon: 'bi-book' },
          { title: 'Average Grade', value: dashboardStats.average_grade, icon: 'bi-star' },
          { title: 'Results Uploaded', value: dashboardStats.results_uploaded, icon: 'bi-check-circle' }
        ];
      } catch (error) {
        alert("Failed to load dashboard stats. Please try again.");
      }
    }
  };
};


window.recentActivities = function() {
  return {
      activities: [], // Holds the list of activities

      // Method to fetch recent activities from the API
      async fetchActivities() {
          try {
              // Fetch recent activities from the API
              const activities = await dispatchRequest("recentActivities", "GET", "/api/activities/recent");
              
              // Map the response data to displayable activity structure
              this.activities = activities.map(activity => ({
                  title: activity.subject, // Activity subject
                  description: activity.action, // Activity action/description
                  time: formatTime(activity.timestamp), // Format the timestamp
                  icon: activity.icon || 'bi-clock' // Default icon if none is provided
              }));
          } catch (error) {
              // Display an alert with a more descriptive error message
              console.error("Error fetching recent activities:", error);
              alert("Failed to load recent activities. Please try again.");
          }
      }
  };
};

window.logout = function() {
  return {
      // Method to fetch recent activities from the API
      async sendLogout() {
          await dispatchRequest("logout", "POST", "/api/token/logout", {refresh: TokenStore.getRefreshToken()});
          TokenStore.clearTokens();

          toastSuccess("Session has been logged out successfully", "center", function() {
            window.location.href = "/";
          });
      }
  };
};

window.userDetails = function() {
  return {
      user: {

      }, // Holds the list of activities

      // Method to fetch recent activities from the API
      async fetchUserDetails() {
          try {
              // Fetch recent activities from the API
              const user = await dispatchRequest("fetchUserDetails", "GET", "/api/user/me");
              
              // Map the response data to displayable activity structure
              this.user = user;

          } catch (error) {
            toastError(
             "Your session has expired due to inactivity. You will be logged out.",
              "center"
            );

            setTimeout(function() {
              window.location.href = "/";
            }, 5000);
          }
      }
  };
};


window.studentList = function() {
  return {
    students: [], // Array to hold students data
    searchTerm: '',
    page: 1, // Current page for pagination
    totalPages: 1, // Total number of pages for pagination
    loading: false,

    async generateSpreadsheet(id) {
      this.loading = true;  // Show loading indicator
      try {
  
    
        // Send the POST request to the backend to generate the spreadsheet
        const response = await dispatchRequest(
          "generateResult",
          "POST",
          `/api/students/${id}/spreadsheet`,
          false
        );
    
        // Check if the response is OK and if the content type is Excel
        // Create a Blob from the response
        const blob = await response.blob();
          
        // Create a URL for the Blob and trigger download
        const downloadUrl = URL.createObjectURL(blob);
        
        // Create a temporary anchor element to trigger the download
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = `student_${id}_results.xlsx`;  // Name the file for download
        document.body.appendChild(a);
        a.click();  // Programmatically trigger the download
        document.body.removeChild(a);  // Clean up the DOM
  
        // Clean up the Blob URL
        URL.revokeObjectURL(downloadUrl);
        
      } catch (error) {
        // Handle errors and show an error message to the user
        this.loading = false;
        console.error("Error generating spreadsheet:", error);
        toastError(`Error generating spreadsheet: ${error.message || "Unexpected error"}`, "center");
      } finally {
        // Ensure loading state is reset
        this.loading = false;
      }
    },    

    // Method to fetch student records
    async fetchRecords() {
      this.loading = true;
      try {
        const response = await dispatchRequest("studentList", "GET", `/api/students?page=${this.page}&search_term=${this.searchTerm}`);
        this.students = response.results; // Students list
        this.totalPages = Math.ceil(response.count / 10); // Total pages based on count and page size (10 per page)
        
        setTimeout(() => {
          this.loading = false;
        }, 1000)

      } catch (error) {
        this.loading = false;
        console.error("Error fetching student records:", error);
      }

    },

    // Pagination methods
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchRecords(); // Fetch new records for the previous page
      }
    },

    nextPage() {
      if (this.page < this.totalPages) {
        this.page++;
        this.fetchRecords(); // Fetch new records for the next page
      }
    }
  };
};


window.uploadStudent = function() {
  return {
    loading: false,
    file: null,
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Method to upload student records from the Excel file
    async uploadFile() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);

        // Send the request
        const response = await dispatchRequest(
          "uploadStudentsFromFile",
          "POST",
          `/api/students/upload`,
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);
          
          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach(error => {
            errorMessage += `${error.error} for matric number ${error.matric_number || 'unknown'}\n`;
          });

          // Show the error message first
          toastError(errorMessage, "right");
        }

        // If no errors, show success message
        if (!this.errors.length) {
          toastSuccess("Student records uploaded successfully!", "center", () => {
            this.loading = false;
            location.reload(true);
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
          console.log("Error uploading student records:", error);
        }
      } finally {
        this.loading = false;
      }
    },
  };
};

window.addStudent = function () {
  return {
    loading: false,
    errors: {}, // Store field-specific and general errors
    successMessage: "", // Success message for successful submissions
    studentData: {
      firstName: "",
      lastName: "",
      matricNumber: "",
      department: "",
      email: "",
      level: "",
      dateOfBirth: "",
    },

    // Method to add a new student
    async addStudent() {
      // Clear previous errors and messages
      this.errors = {};
      this.successMessage = "";

      // Validate input fields
      const requiredFields = [
        "firstName",
        "lastName",
        "matricNumber",
        "department",
        "email",
        "level",
        "dateOfBirth",
      ];

      const missingFields = requiredFields.filter(
        (field) => !this.studentData[field]
      );

      if (missingFields.length > 0) {
        this.errors.general =
          "Please fill out all the required fields.";
        missingFields.forEach((field) => {
          this.errors[field] = `${field.replace(
            /([A-Z])/g,
            " $1"
          )} is required.`; // Converts camelCase to readable text
        });
        return;
      }

      this.loading = true;

      // Prepare the payload
      const payload = {
        first_name: this.studentData.firstName,
        last_name: this.studentData.lastName,
        matric_number: this.studentData.matricNumber,
        email: this.studentData.email,
        department: this.studentData.department,
        level: this.studentData.level,
        date_of_birth: this.studentData.dateOfBirth,
      };

      try {
        // Send the API request
        const response = await dispatchRequest(
          "addStudent", // Unique key for request
          "POST", // HTTP method
          `/api/students`, // Endpoint
          payload // Payload data
        );

        // Handle success
        this.successMessage = "Student added successfully!";
        this.errors = {}; // Clear errors
      } catch (error) {
        // Handle API errors
        if (error?.data) {
          const apiErrors = error.data;

          // Map errors to `errors` object
          this.errors = {};
          for (const [field, messages] of Object.entries(apiErrors)) {
            this.errors[field] = messages[0]; // Use the first error message
          }
        } else {
          this.errors.general =
            error?.data?.error || "An unexpected error occurred.";
        }

        this.successMessage = ""; // Clear success message
      } finally {
        this.loading = false;
      }
    },
  };
};



window.semesterList = function() {
  return {
      semesters: [], // Initialize the semesters array
      loading: false,
      searchTerm: '',
      page: 1, // You can set a default page number if needed
      async fetchRecords() {
          this.loading = true;

          try {
              const response = await dispatchRequest(
                  "semesterList2",  // This would be the action name or identifier
                  "GET",
                  `/api/semesters?page=${this.page}&search_term=${this.searchTerm}`
              );

              if (response && response.results) {
                  this.semesters = response.results;  // Assign the fetched data to semesters
              } else {
                  this.semesters = [];  // Ensure semesters is set to an empty array if no results
              }
          } catch (error) {
              console.error("Error fetching semesters:", error);
              this.semesters = []; // Set to empty array on error
          } finally {
              this.loading = false;  // Set loading to false after the request completes
          }
      }
  };
}


window.addSemester = function() {
  return {
    semesterData: {
      name: "",
      description: "",
      startDate: "",
      endDate: "",
      isActive: true,
    },
    errors: {},
    loading: false,
    successMessage: "",
    
    async addSemester() {
      this.loading = true;
      this.errors = {};
      this.successMessage = "";

      try {
        // Sending the POST request to add a semester using dispatchRequest
        const response = await dispatchRequest("semesterList", "POST", "/api/semesters/", {
          name: this.semesterData.name,
          description: this.semesterData.description,
          start_date: this.semesterData.startDate,
          end_date: this.semesterData.endDate,
          is_active: this.semesterData.isActive,
        });

        // On success, update success message and reset form data
        this.successMessage = "Semester added successfully!";
        this.semesterData = {
          name: "",
          description: "",
          startDate: "",
          endDate: "",
          isActive: true,
        };

      } catch (error) {
        // Handle any errors that occur during the request
        this.errors = error.response?.data || { general: "An error occurred. Please try again." };
      } finally {
        // Always reset the loading state
        this.loading = false;
      }
    },
  };
}


window.uploadSemester = function () {
  return {
    loading: false,
    file: null,
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Method to upload semester records from the Excel file
    async uploadFile() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);

        // Send the request
        const response = await dispatchRequest(
          "uploadSemestersFromFile",
          "POST",
          `/api/semesters/upload`,
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);

          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach((error) => {
            errorMessage += `${error.error} for semester ${error.name || "unknown"}\n`;
          });

          // Show the error message
          toastError(errorMessage, "right");
        }

        // If no errors, show success message
        if (!this.errors.length) {
          toastSuccess("Semester records uploaded successfully!", "center", () => {
            this.loading = false;
            location.reload(true);
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
          console.log("Error uploading semester records:", error);
        }
      } finally {
        this.loading = false;
      }
    },
  };
};


window.uploadDepartment = function () {
  return {
    loading: false,
    file: null,
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Method to upload department records from the Excel file
    async uploadFile() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);

        // Send the request
        const response = await dispatchRequest(
          "uploadDepartmentsFromFile",
          "POST",
          `/api/departments/upload`,
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);

          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach((error) => {
            errorMessage += `${error.error} for department ${error.name || "unknown"}\n`;
          });

          // Show the error message
          toastError(errorMessage, "right");
        }

        // If no errors, show success message
        if (!this.errors.length) {
          toastSuccess("Department records uploaded successfully!", "center", () => {
            this.loading = false;
            location.reload(true);
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
          console.log("Error uploading department records:", error);
        }
      } finally {
        this.loading = false;
      }
    },
  };
};

window.departmentList = function() {
  return {
    departments: [], // Array to hold department data
    searchTerm: '', // Search term for filtering departments
    page: 1, // Current page for pagination
    totalPages: 1, // Total number of pages for pagination
    loading: false, // Loading state

    // Method to fetch department records
    async fetchRecords() {
      this.loading = true;
      try {
        const response = await dispatchRequest("departmentList", "GET", `/api/departments?page=${this.page}&search_term=${this.searchTerm}`);
        this.departments = response.results; // Department list
        this.totalPages = Math.ceil(response.count / 10); // Total pages based on count and page size (10 per page)
        
        setTimeout(() => {
          this.loading = false;
        }, 1000); // Delay loading state for a better user experience

      } catch (error) {
        this.loading = false;
        console.error("Error fetching department records:", error);
      }
    },

    // Pagination methods
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchRecords(); // Fetch new records for the previous page
      }
    },

    nextPage() {
      if (this.page < this.totalPages) {
        this.page++;
        this.fetchRecords(); // Fetch new records for the next page
      }
    }
  };
};


window.addDepartment = function() {
  return {
    departmentData: {
      name: "",  // Department name (e.g., "Computer Science")
      description: "",  // A brief description of the department
      isActive: true,  // Is the department active?
      code: "",
    },
    errors: {},
    loading: false,
    successMessage: "",

    async addDepartment() {
      this.loading = true;
      this.errors = {};
      this.successMessage = "";
    
      try {
        // Sending the POST request to add a department using dispatchRequest
        const response = await dispatchRequest("departmentList", "POST", "/api/departments/", {
          name: this.departmentData.name,
          code: this.departmentData.code,
          description: this.departmentData.description,
          is_active: this.departmentData.isActive,
        });
    
        // On success, update success message and reset form data
        this.successMessage = "Department added successfully!";
        this.departmentData = {
          name: "",
          description: "",
          isActive: true,
        };
    
      } catch (error) {
        console.error("Error adding department:", error);  // Log the error for better visibility
        // Handle any errors that occur during the request
        this.errors = error.response?.data || { general: "An error occurred. Please try again." };
    
        // Optionally, display the error response in the console to further debug
        if (error.response) {
          console.log("API Error Response:", error.response.data);
        }
      } finally {
        // Always reset the loading state
        this.loading = false;
      }
    },
  };
}



window.uploadSession = function () {
  return {
    loading: false,
    file: null,
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Method to upload session records from the Excel file
    async uploadFile() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);

        // Send the request
        const response = await dispatchRequest(
          "uploadSessionsFromFile",
          "POST",
          `/api/sessions/upload`,
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);

          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach((error) => {
            errorMessage += `${error.error} for session ${error.name || "unknown"}\n`;
          });

          // Show the error message
          toastError(errorMessage, "right");
        }

        // If no errors, show success message
        if (!this.errors.length) {
          toastSuccess("Session records uploaded successfully!", "center", () => {
            this.loading = false;
            location.reload(true);
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
          console.log("Error uploading session records:", error);
        }
      } finally {
        this.loading = false;
      }
    },
  };
};

window.sessionList = function() {
  return {
    sessions: [], // Array to hold session data
    searchTerm: '', // Search term for filtering sessions
    page: 1, // Current page for pagination
    totalPages: 1, // Total number of pages for pagination
    loading: false, // Loading state

    // Method to fetch session records
    async fetchRecords() {
      this.loading = true;
      try {
        const response = await dispatchRequest("sessionList", "GET", `/api/sessions?page=${this.page}&search_term=${this.searchTerm}`);
        this.sessions = response.results || []; // Session list
        this.totalPages = Math.ceil(response.count / 10); // Total pages based on count and page size (10 per page)
        
        setTimeout(() => {
          this.loading = false;
        }, 1000); // Delay loading state for a better user experience

      } catch (error) {
        this.loading = false;
        console.error("Error fetching session records:", error);
      }
    },

    // Pagination methods
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchRecords(); // Fetch new records for the previous page
      }
    },

    nextPage() {
      if (this.page < this.totalPages) {
        this.page++;
        this.fetchRecords(); // Fetch new records for the next page
      }
    }
  };
};


window.addSession = function() {
  return {
    sessionData: {
      name: "",  // Session name (e.g., "2023/2024")
      semester: 1,  // The associated semester, e.g., 1
      startDate: "",  // Start date of the session
      endDate: "",  // End date of the session
      isActive: true,  // Is the session active?
    },
    errors: {},
    loading: false,
    successMessage: "",

    async addSession() {
      this.loading = true;
      this.errors = {};
      this.successMessage = "";

      try {
        // Sending the POST request to add a session using dispatchRequest
        const response = await dispatchRequest("sessionList", "POST", "/api/sessions/", {
          name: this.sessionData.name,
          semester: this.sessionData.semester,  // Add the semester value
          start_date: this.sessionData.startDate,
          end_date: this.sessionData.endDate,
          is_active: this.sessionData.isActive,
        });

        // On success, update success message and reset form data
        this.successMessage = "Session added successfully!";
        this.sessionData = {
          name: "",
          semester: 1,  // Reset the semester back to the default value
          startDate: "",
          endDate: "",
          isActive: true,
        };

      } catch (error) {
        // Handle any errors that occur during the request
        this.errors = error.response?.data || { general: "An error occurred. Please try again." };
      } finally {
        // Always reset the loading state
        this.loading = false;
      }
    },
  };
}

window.courseList = function() {
  return {
    courses: [], // Array to hold the course data
    searchTerm: '', // Search term for filtering courses
    page: 1, // Current page for pagination
    totalPages: 1, // Total number of pages for pagination
    loading: false, // Loading state

    // Method to fetch course records
    async fetchRecords() {
      this.loading = true;
      try {
        const response = await dispatchRequest("courseList", "GET", `/api/courses?page=${this.page}&search_term=${this.searchTerm}`);
        
        this.courses = response.results || []; // Ensure courses is an array
        const count = response.count ?? 1; // Use 0 as fallback for undefined/null count
        this.totalPages = Math.ceil(count / 10); // Calculate total pages based on count
        
        setTimeout(() => {
          this.loading = false;
        }, 1000); // Delay loading state for better user experience

      } catch (error) {
        this.loading = false;
        console.error("Error fetching course records:", error);
      }
    },

    // Pagination methods
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchRecords(); // Fetch new records for the previous page
      }
    },

    nextPage() {
      if (this.page < this.totalPages) {
        this.page++;
        this.fetchRecords(); // Fetch new records for the next page
      }
    }
  };
};

window.addCourse = function () {
  return {
    loading: false,
    errors: {}, // Store field-specific and general errors
    successMessage: "", // Success message for successful submissions
    courseData: {
      name: "",
      code: "",
      department: null,  // Assuming department ID
      session: null,     // Assuming session ID
      creditUnits: 3,
      description: "",
      isActive: true,
    },

    // Method to add a new course
    async addCourse() {
      // Clear previous errors and messages
      this.errors = {};
      this.successMessage = "";

      // Validate input fields
      const requiredFields = [
        "name",
        "code",
        "department",
        "session",
      ];

      const missingFields = requiredFields.filter(
        (field) => !this.courseData[field]
      );

      if (missingFields.length > 0) {
        this.errors.general = "Please fill out all the required fields.";
        missingFields.forEach((field) => {
          this.errors[field] = `${field.replace(
            /([A-Z])/g,
            " $1"
          )} is required.`; // Converts camelCase to readable text
        });
        return;
      }

      this.loading = true;

      // Prepare the payload to match the Django Course model
      const payload = {
        name: this.courseData.name,
        code: this.courseData.code,
        department: this.courseData.department, // Assumed as the department ID
        session: this.courseData.session,       // Assumed as the session ID
        credit_units: this.courseData.creditUnits,
        description: this.courseData.description,
        is_active: this.courseData.isActive,
      };

      try {
        // Send the API request
        const response = await dispatchRequest(
          "addCourse", // Unique key for request
          "POST", // HTTP method
          `/api/courses`, // Endpoint (make sure this matches your Django URL pattern)
          payload // Payload data
        );

        // Handle success
        this.successMessage = "Course added successfully!";
        this.errors = {}; // Clear errors
      } catch (error) {
        // Handle API errors
        if (error?.data) {
          const apiErrors = error.data;

          // Map errors to `errors` object
          this.errors = {};
          for (const [field, messages] of Object.entries(apiErrors)) {
            this.errors[field] = messages[0]; // Use the first error message
          }
        } else {
          this.errors.general =
            error?.data?.error || "An unexpected error occurred.";
        }

        this.successMessage = ""; // Clear success message
      } finally {
        this.loading = false;
      }
    },
  };
};

window.uploadCourse = function () {
  return {
    loading: false,
    file: null,
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Method to upload course records from the Excel file
    async uploadFile() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);

        // Send the request
        const response = await dispatchRequest(
          "uploadCoursesFromFile",
          "POST",
          `/api/courses/upload`,  // Adjusted endpoint for courses
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);

          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach((error) => {
            errorMessage += `${error.error} for course ${error.code || "unknown"}\n`;
          });

          // Show the error message
          toastError(errorMessage, "right");
        }

        // If no errors, show success message
        if (!this.errors.length) {
          toastSuccess("Course records uploaded successfully!", "center", () => {
            this.loading = false;
            location.reload(true);
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
          console.log("Error uploading course records:", error);
        }
      } finally {
        this.loading = false;
      }
    },
  };
};



window.resultList = function() {
  return {
    results: [], // Array to hold the result data
    searchTerm: '', // Search term for filtering results
    page: 1, // Current page for pagination
    totalPages: 1, // Total number of pages for pagination
    loading: false, // Loading state

    // Method to fetch result records
    async fetchRecords() {
      this.loading = true;
      try {
        const response = await dispatchRequest("resultList", "GET", `/api/results?page=${this.page}&search_term=${this.searchTerm}`);
        
        // Log the response for debugging purposes
        console.log('API Response:', response);

        // Ensure `results` is an array and `count` is valid
        this.results = Array.isArray(response?.results) ? response.results : [];
        
        const count = response?.count ?? 0; // Default to 0 if count is missing
        this.totalPages = Math.ceil(count / 10); // Calculate total pages based on count
        
        setTimeout(() => {
          this.loading = false;
        }, 1000); // Delay loading state for better user experience

      } catch (error) {
        alert("Error loading results");
        this.loading = false;
        console.error("Error fetching result records:", error);
      }
    },

    // Pagination methods
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchRecords(); // Fetch new records for the previous page
      }
    },

    nextPage() {
      if (this.page < this.totalPages) {
        this.page++;
        this.fetchRecords(); // Fetch new records for the next page
      }
    }
  };
};


window.uploadResult = function () {
  return {
    loading: false,
    file: null,
    course: "", // Store selected course
    session: "", // Store selected session
    errors: [], // To store error messages

    // Handle file change (on file selection)
    handleFileChange(event) {
      this.file = event.target.files[0];
    },

    // Handle course selection
    handleCourseChange(event) {
      this.course = event.target.value;
    },

    // Handle session selection
    handleSessionChange(event) {
      this.session = event.target.value;
    },

    // Method to upload course records from the Excel file
    async uploadFile() {
      if (!this.course) {
        toastError("Please select a course before uploading.", "center");
        return;
      }

      if (!this.session) {
        toastError("Please select a session before uploading.", "center");
        return;
      }

      if (!this.file) {
        toastError("Please select a file before uploading.", "center");
        return;
      }

      this.loading = true;
      this.errors = []; // Clear previous errors

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append("file", this.file);
        formData.append("session", this.session);
        formData.append("course", this.course); // Include selected course

        // Send the request
        const response = await dispatchRequest(
          "uploadResultsFromFile",
          "POST",
          `/api/results/upload`, // Adjusted endpoint for courses
          formData
        );

        // Check if there are any errors in the response
        if (response.errors && response.errors.length > 0) {
          this.errors = response.errors; // Capture errors from the response
          console.log("Upload errors:", this.errors);

          // Combine all errors into a single message for display
          let errorMessage = "Some records failed to upload. Errors:\n";
          this.errors.forEach((error) => {
            errorMessage += `${error.error} for course ${error.course_code || "unknown"}\n`;
          });

          // Show the error message
          toastError(errorMessage, "right");

          // Exit the function if there are errors
          return; // Skip success handling if errors exist
        }

        // If no errors, show success message
        toastSuccess("Course records uploaded successfully!", "center", () => {
          this.loading = false;
          location.reload(true);
        });

      } catch (error) {
        // Handle unexpected errors
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors;
        } else {
          toastError(
            error?.data?.error || "An unexpected error occurred.",
            "center"
          );
        }
      } finally {
        this.loading = false;
      }
    },
  };
};


