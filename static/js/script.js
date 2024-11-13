
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
  