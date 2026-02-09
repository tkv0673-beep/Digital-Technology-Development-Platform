import { makeAutoObservable, runInAction } from 'mobx';

class AuthStore {
  user = null;
  accessToken = localStorage.getItem('accessToken');
  refreshToken = localStorage.getItem('refreshToken');
  isLoading = false;
  error = null;

  constructor() {
    makeAutoObservable(this);
    // Загружаем пользователя из localStorage, если он уже сохранён
    try {
      const rawUser = localStorage.getItem('dtp_mock_user_v1');
      if (rawUser) {
        this.user = JSON.parse(rawUser);
      }
    } catch (e) {
      this.user = null;
    }
  }

  async login(username, password) {
    this.isLoading = true;
    this.error = null;
    try {
      runInAction(() => {
        // Мок-логика авторизации: любой логин/пароль, без реального API
        const mockUser = {
          username,
          email: `${username}@example.com`,
          role: username === 'mentor' ? 'mentor' : 'mentee',
          first_name: '',
          last_name: '',
          phone: '',
        };
        this.user = mockUser;
        // Токены нужны только формально для существующего кода
        this.accessToken = 'mock-access-token';
        this.refreshToken = 'mock-refresh-token';
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
        localStorage.setItem('dtp_mock_user_v1', JSON.stringify(mockUser));
        this.isLoading = false;
      });
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = 'Ошибка входа';
        this.isLoading = false;
      });
      return false;
    }
  }

  async register(userData) {
    this.isLoading = true;
    this.error = null;
    try {
      runInAction(() => {
        // Мок-регистрация: сохраняем пользователя только на фронтенде
        const mockUser = {
          username: userData.username,
          email: userData.email,
          role: userData.role || 'mentee',
          first_name: userData.first_name || '',
          last_name: userData.last_name || '',
          phone: userData.phone || '',
        };
        this.user = mockUser;
        this.accessToken = 'mock-access-token';
        this.refreshToken = 'mock-refresh-token';
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
        localStorage.setItem('dtp_mock_user_v1', JSON.stringify(mockUser));
        this.isLoading = false;
      });
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = 'Ошибка регистрации';
        this.isLoading = false;
      });
      return false;
    }
  }

  async loadUser() {
    // В режиме моков просто берём пользователя из localStorage
    try {
      const rawUser = localStorage.getItem('dtp_mock_user_v1');
      if (!rawUser) return;
      const user = JSON.parse(rawUser);
      runInAction(() => {
        this.user = user;
      });
    } catch (e) {
      // игнорируем
    }
  }

  async refreshAccessToken() {
    // Токены моковые — просто возвращаем успех
    return true;
  }

  logout() {
    this.user = null;
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('dtp_mock_user_v1');
  }

  get isAuthenticated() {
    return !!this.user;
  }

  get isMentor() {
    return this.user?.role === 'mentor';
  }
}

export const authStore = new AuthStore();

