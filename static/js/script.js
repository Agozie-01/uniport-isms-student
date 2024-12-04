async fetchStats() {
  try {
      const dashboardStats = await dispatchRequest("dashboardStats", "GET", "/api/dashboard/stats");

      this.stats = [
          { title: 'Total Students', value: dashboardStats.total_students, icon: 'users' },
          { title: 'Total Courses', value: dashboardStats.total_courses, icon: 'book-open' },
          { title: 'Average Grade', value: dashboardStats.average_grade, icon: 'star' },
          { title: 'Results Uploaded', value: dashboardStats.results_uploaded, icon: 'clock' }
      ];

      // Wait for Alpine.js to finish rendering the DOM
      this.$nextTick(() => {
          setTimeout(() => {
              feather.replace(); // Apply Feather icons after Alpine.js renders the DOM
          }, 100);
      });

  } catch (error) {
      console.error("Error loading dashboard stats:", error);
      alert("Failed to load dashboard stats. Please try again.");
  }
}
