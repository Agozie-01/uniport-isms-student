
// Utility to determine the storage type
const storage = window.localStorage; // Use sessionStorage if session-only persistence is needed

// Token Utility Functions
const TokenStore = {
  /**
   * Store tokens in storage
   * @param {string} accessToken - The access token
   * @param {string} refreshToken - The refresh token
   */
  set(accessToken, refreshToken) {
    storage.setItem("accessToken", accessToken);
    storage.setItem("refreshToken", refreshToken);
  },

  /**
   * Retrieve the access token
   * @returns {string | null} - The access token or null if not found
   */
  getAccessToken() {
    return storage.getItem("accessToken");
  },

  /**
   * Retrieve the refresh token
   * @returns {string | null} - The refresh token or null if not found
   */
  getRefreshToken() {
    return storage.getItem("refreshToken");
  },

  /**
   * Remove both tokens from storage
   */
  clearTokens() {
    storage.removeItem("accessToken");
    storage.removeItem("refreshToken");
  },
};

// General Data Utility Functions
const DataStore = {
  /**
   * Store data in storage
   * @param {string} key - The key to store the data under
   * @param {any} value - The value to store (will be stringified)
   */
  set(key, value) {
    storage.setItem(key, JSON.stringify(value));
  },

  /**
   * Retrieve data from storage
   * @param {string} key - The key to retrieve the data for
   * @returns {any | null} - The parsed data or null if not found
   */
  get(key) {
    const value = storage.getItem(key);
    return value ? JSON.parse(value) : null;
  },

  /**
   * Remove data from storage
   * @param {string} key - The key of the data to remove
   */
  unset(key) {
    storage.removeItem(key);
  },

  clearAll() {
    storage.clear();
  },

  clearByKeys(keys) {
    // Ensure the input is an array
    if (!Array.isArray(keys)) {
        console.error("Error: Keys must be provided as an array.");
        return;
    }

    // Loop through the keys and remove each one
    keys.forEach((key) => {
        if (localStorage.getItem(key) !== null) {
            localStorage.removeItem(key);
            console.log(`Key "${key}" removed from localStorage.`);
        } else {
            console.warn(`Key "${key}" does not exist in localStorage.`);
        }
    });
  }
};
