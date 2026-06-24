import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const register = (data) =>
  axios.post(`${API_URL}/auth/register`, data);

export const login = (data) =>
  axios.post(`${API_URL}/auth/login`, data);

export const getMe = (token) =>
  axios.get(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });