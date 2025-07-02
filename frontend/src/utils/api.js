import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const registerUser = async (userData) => {
  return await axios.post(`${API_BASE_URL}/users/`, userData, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    withCredentials: true  
  });
};
