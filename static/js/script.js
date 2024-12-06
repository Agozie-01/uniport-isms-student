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
              // Display an alert with a more descriptive error message
              console.error("Error fetching user details:", error);
              alert("Failed to load user details. Please try again.");
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
          });
        }

      } catch (error) {
        // Check if server sent specific error messages
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors; // Capture errors from server response
          console.log("Upload errors:", this.errors);
        } else {
          toastError(
            error?.response?.data?.error || "An unexpected error occurred.",
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
