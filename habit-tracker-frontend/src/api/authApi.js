import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const register = (data) => {
  return axios.post(`${API_URL}/auth/register`, data);
};

export const login = (formData) => {
  return axios.post(`${API_URL}/auth/login`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export const getMe = (token) => {
  return axios.get(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};