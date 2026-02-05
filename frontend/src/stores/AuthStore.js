import { makeAutoObservable, runInAction } from 'mobx';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class AuthStore {
  user = null;
  accessToken = localStorage.getItem('accessToken');
  refreshToken = localStorage.getItem('refreshToken');
  isLoading = false;
  error = null;

  constructor() {
    makeAutoObservable(this);
    if (this.accessToken) {
      this.loadUser();
    }
  }

  async login(username, password) {
    this.isLoading = true;
    this.error = null;
    try {
      const response = await axios.post(`${API_URL}/auth/login/`, {
        username,
        password,
      });
      
      runInAction(() => {
        this.accessToken = response.data.access_token;
        this.refreshToken = response.data.refresh_token;
        this.user = response.data.user;
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
        this.isLoading = false;
      });
      
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = error.response?.data?.error || 'Ошибка входа';
        this.isLoading = false;
      });
      return false;
    }
  }

  async register(userData) {
    this.isLoading = true;
    this.error = null;
    try {
      const response = await axios.post(`${API_URL}/auth/register/`, userData);
      
      runInAction(() => {
        this.accessToken = response.data.access_token;
        this.refreshToken = response.data.refresh_token;
        this.user = response.data.user;
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
        this.isLoading = false;
      });
      
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = error.response?.data || 'Ошибка регистрации';
        this.isLoading = false;
      });
      return false;
    }
  }

  async loadUser() {
    if (!this.accessToken) return;
    
    try {
      const response = await axios.get(`${API_URL}/auth/me/`, {
        headers: { Authorization: `Bearer ${this.accessToken}` },
      });
      runInAction(() => {
        this.user = response.data;
      });
    } catch (error) {
      // Token might be expired, try refresh
      if (error.response?.status === 401) {
        await this.refreshAccessToken();
      }
    }
  }

  async refreshAccessToken() {
    if (!this.refreshToken) {
      this.logout();
      return;
    }
    
    try {
      const response = await axios.post(`${API_URL}/auth/refresh/`, {
        refresh_token: this.refreshToken,
      });
      
      runInAction(() => {
        this.accessToken = response.data.access_token;
        this.refreshToken = response.data.refresh_token;
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
      });
      
      return true;
    } catch (error) {
      this.logout();
      return false;
    }
  }

  logout() {
    this.user = null;
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  get isAuthenticated() {
    return !!this.user;
  }

  get isMentor() {
    return this.user?.role === 'mentor';
  }
}

export const authStore = new AuthStore();

