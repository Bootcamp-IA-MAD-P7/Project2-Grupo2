const API_BASE_URL = "[link removed]";

/**
 * Helper to get the auth token from localStorage
 */
function getAuthHeader() {
    const token = localStorage.getItem('access_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

async function getData(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: { ...getAuthHeader() }
    });
    
    if (response.status === 401) {
        window.location.href = 'login.html';
        return;
    }
    
    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
    return await response.json();
}

async function postData(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            ...getAuthHeader()
        },
        body: JSON.stringify(data)
    });

    if (response.status === 401) {
        window.location.href = 'login.html';
        return;
    }

    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
    return await response.json();}