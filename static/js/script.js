
/* 
document.addEventListener('alpine:init', () => {
    Alpine.data('fetchDataComponent', () => ({
      data: null,
      error: null,
      loading: false,
      fetchData() {
        this.loading = true;
        this.error = null;
  
        fetch('https://api.test.swita.ng')  // Replace with your API endpoint
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(result => {
            this.data = result;
            this.loading = false;
          })
          .catch(error => {
            this.error = 'Failed to fetch data: ' + error.message;
            this.loading = false;
          });
      }
    }));
});
 */

window.onload = function () {
  loadDashboardData();
};


// Function to initialize the dashboard by loading all required data
async function loadDashboardData() {
  try {
    // Fetch data in parallel using Promise.all
    const [userDetails, dashboardStats, recentActivities, coursePerformanceTrend] = await Promise.all([
      dispatchRequest("userDetails", "GET", "/api/user/me"),
      dispatchRequest("dashboardStats", "GET", "/api/dashboard-stats/"),
      dispatchRequest("recentActivities", "GET", "/api/recent-activities/"),
      dispatchRequest("coursePerformanceTrend", "GET", "/api/course-performance-trend/"),
    ]);

    console.log("Dashboard data loaded successfully");

    // Render the fetched data
    renderUserDetails(userDetails);
    renderDashboardStats(dashboardStats);
    renderRecentActivities(recentActivities);
    renderCoursePerformanceTrend(coursePerformanceTrend);
  } catch (error) {
    console.error("Error loading dashboard data:", error);
    alert("Failed to load dashboard data. Please try again.");
  }
}


// Function to render user details
function renderUserDetails(userDetails) {
  const userElement = document.getElementById("user-details");
  if (userElement) {
    userElement.textContent = `Welcome, ${userDetails.name}`;
  } else {
    console.warn("Element 'user-details' not found in the DOM.");
  }
}

// Function to render dashboard statistics
function renderDashboardStats(stats) {
  const statsElement = document.getElementById("dashboard-stats");
  if (statsElement) {
    statsElement.textContent = `Total Courses: ${stats.totalCourses}, Completed: ${stats.completedCourses}`;
  } else {
    console.warn("Element 'dashboard-stats' not found in the DOM.");
  }
}

// Function to render recent activities
function renderRecentActivities(activities) {
  const activitiesElement = document.getElementById("recent-activities");
  if (activitiesElement) {
    activitiesElement.innerHTML = activities
      .map((activity) => `<li>${activity}</li>`)
      .join("");
  } else {
    console.warn("Element 'recent-activities' not found in the DOM.");
  }
}

// Function to render course performance trend
function renderCoursePerformanceTrend(trend) {
  const trendElement = document.getElementById("course-performance-trend");
  if (trendElement) {
    trendElement.textContent = `Performance Trend: ${trend.trend}`;
  } else {
    console.warn("Element 'course-performance-trend' not found in the DOM.");
  }
}


  