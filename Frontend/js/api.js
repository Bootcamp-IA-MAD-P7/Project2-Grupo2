const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

async function apiRequest(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      ...options
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    if (response.status === 204) {
      return null;
    }

    return await response.json();

  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

async function getData(endpoint) {
  return apiRequest(endpoint);
}

async function postData(endpoint, data) {
  return apiRequest(endpoint, {
    method: "POST",
    body: JSON.stringify(data)
  });
}