import { createContext, useEffect, useState } from "react";
import { getMe, login as loginRequest } from "../api/authApi";
import { getToken, removeToken, saveToken } from "../utils/token";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await loginRequest(formData);
    const token = response.data.access_token;

    saveToken(token);

    const meResponse = await getMe(token);
    setUser(meResponse.data);

    return meResponse.data;
  };

  const logout = () => {
    removeToken();
    setUser(null);
  };

  useEffect(() => {
    const loadUser = async () => {
      const token = getToken();

      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await getMe(token);
        setUser(response.data);
      } catch {
        removeToken();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}