
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
      dispatchRequest("dashboardStats", "GET", "/api/dashboard/stats"),
      dispatchRequest("recentActivities", "GET", "/api/activities/recent"),
      dispatchRequest("coursePerformanceTrend", "GET", "/api/courses/performance-trend"),
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

// Function to render dashboard statistics as cards
function renderDashboardStats(stats) {
  const statsElement = document.getElementById("dashboard-stats");

  if (statsElement) {
    // Clear any existing content
    statsElement.innerHTML = '';

    // Define the statistics for the cards
    const statistics = [
      { title: 'Total Students', value: stats.total_students, icon: 'users' },
      { title: 'Total Courses', value: stats.total_courses, icon: 'book-open' },
      { title: 'Average Grade', value: stats.average_grade, icon: 'star' },
      { title: 'Results Uploaded', value: stats.results_uploaded, icon: 'clock' }
    ];

    // Loop through the statistics and create cards for each
    statistics.forEach(stat => {
      const card = createStatCard(stat.title, stat.value, stat.icon);
      statsElement.appendChild(card);
    });
  } else {
    console.warn("Element 'dashboard-stats' not found in the DOM.");
  }
}

// Function to create a single stat card
function createStatCard(title, value, icon) {
  const card = document.createElement("div");
  card.classList.add("col-md-3");

  // Create the card element
  const cardElement = document.createElement("div");
  cardElement.classList.add("card", "rounded-lg");
  cardElement.style.border = "none";
  cardElement.style.boxShadow = "none";

  // Create the card body
  const cardBody = document.createElement("div");
  cardBody.classList.add("card-body");

  // Create the row inside the card body
  const row = document.createElement("div");
  row.classList.add("row", "d-flex", "align-items-center");

  // Create the icon column
  const iconColumn = document.createElement("div");
  iconColumn.classList.add("col-auto");

  const statIcon = document.createElement("div");
  statIcon.classList.add("stat", "text-primary");

  const iconElement = document.createElement("i");
  iconElement.classList.add("align-middle");
  iconElement.setAttribute("data-feather", icon);

  statIcon.appendChild(iconElement);
  iconColumn.appendChild(statIcon);

  // Create the text column
  const textColumn = document.createElement("div");
  textColumn.classList.add("col", "mt-2");

  const cardTitle = document.createElement("h5");
  cardTitle.classList.add("card-title");
  cardTitle.textContent = title;

  const cardValue = document.createElement("h4");
  cardValue.classList.add("mt-1", "card-subtitle");
  cardValue.textContent = value;

  textColumn.appendChild(cardTitle);
  textColumn.appendChild(cardValue);

  // Append columns to the row
  row.appendChild(iconColumn);
  row.appendChild(textColumn);

  // Append the row to the card body
  cardBody.appendChild(row);

  // Append the card body to the card
  cardElement.appendChild(cardBody);

  // Append the card to the column
  card.appendChild(cardElement);

  return card;
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


  