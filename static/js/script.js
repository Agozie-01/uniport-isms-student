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







