/**
 * Application constants
 */
export const ROLES = {
  MENTOR: 'mentor',
  MENTEE: 'mentee',
};

export const DIFFICULTY_LEVELS = {
  BASIC: 'basic',
  ADVANCED: 'advanced',
};

export const DIFFICULTY_LABELS = {
  [DIFFICULTY_LEVELS.BASIC]: 'Базовый',
  [DIFFICULTY_LEVELS.ADVANCED]: 'Расширенный',
};

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login/',
    REGISTER: '/api/auth/register/',
    REFRESH: '/api/auth/refresh/',
    LOGOUT: '/api/auth/logout/',
  },
  COURSES: {
    LIST: '/api/courses/',
    DETAIL: (id) => `/api/courses/${id}/`,
    ENROLL: (id) => `/api/courses/${id}/enroll/`,
    PROGRESS: (id) => `/api/courses/${id}/progress/`,
    LESSONS: (id) => `/api/courses/${id}/lessons/`,
  },
  LESSONS: {
    COMPLETE: (id) => `/api/lessons/${id}/complete/`,
  },
  CHATBOT: {
    MESSAGE: '/api/chatbot/message/',
    CONTEXT: (lessonId) => `/api/chatbot/context/${lessonId}/`,
    HISTORY: '/api/chatbot/history/',
  },
};

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
};

