import axios from "axios";
import { getToken } from "../utils/token";

const API_URL = import.meta.env.VITE_API_URL;

export const getHabits = async () => {
  const token = getToken();

  const response = await axios.get(`${API_URL}/habits`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const createHabit = async (data) => {
  const token = getToken();

  const response = await axios.post(`${API_URL}/habits`, data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const deleteHabit = async (habitId) => {
    const token = getToken();

    await axios.delete(`${API_URL}/habits/${habitId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
};
  