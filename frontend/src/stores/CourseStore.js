import { makeAutoObservable, runInAction } from 'mobx';
import axios from 'axios';
import { authStore } from './AuthStore';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class CourseStore {
  courses = [];
  currentCourse = null;
  currentLesson = null;
  isLoading = false;
  error = null;

  constructor() {
    makeAutoObservable(this);
  }

  get axiosConfig() {
    return {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    };
  }

  async loadCourses(difficulty = null) {
    this.isLoading = true;
    this.error = null;
    try {
      const params = difficulty ? { difficulty } : {};
      const response = await axios.get(`${API_URL}/courses/`, {
        params,
        ...this.axiosConfig,
      });
      
      runInAction(() => {
        this.courses = response.data.results || response.data;
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = error.response?.data?.error || 'Ошибка загрузки курсов';
        this.isLoading = false;
      });
    }
  }

  async loadCourse(id) {
    this.isLoading = true;
    this.error = null;
    try {
      const response = await axios.get(`${API_URL}/courses/${id}/`, this.axiosConfig);
      
      runInAction(() => {
        this.currentCourse = response.data;
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = error.response?.data?.error || 'Ошибка загрузки курса';
        this.isLoading = false;
      });
    }
  }

  async enrollInCourse(courseId) {
    try {
      await axios.post(
        `${API_URL}/courses/${courseId}/enroll/`,
        {},
        this.axiosConfig
      );
      await this.loadCourse(courseId);
      return true;
    } catch (error) {
      this.error = error.response?.data?.error || 'Ошибка записи на курс';
      return false;
    }
  }

  async loadLesson(courseId, lessonId) {
    this.isLoading = true;
    this.error = null;
    try {
      const courseResponse = await axios.get(
        `${API_URL}/courses/${courseId}/`,
        this.axiosConfig
      );
      const lesson = courseResponse.data.lessons?.find(l => l.id === parseInt(lessonId));
      
      runInAction(() => {
        this.currentLesson = lesson;
        this.currentCourse = courseResponse.data;
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = error.response?.data?.error || 'Ошибка загрузки урока';
        this.isLoading = false;
      });
    }
  }

  async completeLesson(lessonId, score = null) {
    try {
      await axios.post(
        `${API_URL}/lessons/${lessonId}/complete/`,
        { score },
        this.axiosConfig
      );
      return true;
    } catch (error) {
      this.error = error.response?.data?.error || 'Ошибка завершения урока';
      return false;
    }
  }
}

export const courseStore = new CourseStore();

