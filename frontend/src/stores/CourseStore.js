import { makeAutoObservable, runInAction } from 'mobx';
import { MOCK_COURSES } from '../mocks/courses';

class CourseStore {
  courses = [];
  currentCourse = null;
  currentLesson = null;
  isLoading = false;
  error = null;
  // Прогресс хранится в памяти и в localStorage
  progressByCourse = {};

  constructor() {
    makeAutoObservable(this);
    this.loadProgressFromStorage();
  }

  loadProgressFromStorage() {
    try {
      const raw = localStorage.getItem('dtp_course_progress_v1');
      if (raw) {
        this.progressByCourse = JSON.parse(raw);
      }
    } catch (e) {
      // игнорируем ошибки парсинга и стартуем с нуля
      this.progressByCourse = {};
    }
  }

  saveProgressToStorage() {
    try {
      localStorage.setItem('dtp_course_progress_v1', JSON.stringify(this.progressByCourse));
    } catch (e) {
      // в режиме демо можем игнорировать ошибки записи
    }
  }

  getEnrollment(courseId) {
    const progress = this.progressByCourse[courseId];
    if (!progress) return null;
    return {
      progress_percentage: progress.progressPercentage || 0,
      completed_lessons: progress.completedLessons || [],
    };
  }

  async loadCourses(difficulty = null) {
    this.isLoading = true;
    this.error = null;
    // Имитация загрузки с сервера
    setTimeout(() => {
      runInAction(() => {
        let list = MOCK_COURSES;
        if (difficulty) {
          list = list.filter((c) => c.difficulty === difficulty);
        }
        this.courses = list.map((course) => ({
          ...course,
          enrollment: this.getEnrollment(course.id),
        }));
        this.isLoading = false;
      });
    }, 400);
  }

  async loadCourse(id) {
    this.isLoading = true;
    this.error = null;
    setTimeout(() => {
      runInAction(() => {
        const course = MOCK_COURSES.find((c) => c.id === id);
        if (!course) {
          this.error = 'Курс не найден';
          this.currentCourse = null;
        } else {
          this.currentCourse = {
            ...course,
            enrollment: this.getEnrollment(course.id),
          };
        }
        this.isLoading = false;
      });
    }, 300);
  }

  async enrollInCourse(courseId) {
    const existing = this.progressByCourse[courseId] || {
      completedLessons: [],
      progressPercentage: 0,
    };
    this.progressByCourse[courseId] = existing;
    this.saveProgressToStorage();
    // Обновляем текущий курс/список
    if (this.currentCourse?.id === courseId) {
      this.currentCourse = {
        ...this.currentCourse,
        enrollment: this.getEnrollment(courseId),
      };
    }
    this.courses = this.courses.map((c) =>
      c.id === courseId ? { ...c, enrollment: this.getEnrollment(courseId) } : c
    );
    return true;
  }

  async loadLesson(courseId, lessonId) {
    this.isLoading = true;
    this.error = null;
    setTimeout(() => {
      runInAction(() => {
        const course = MOCK_COURSES.find((c) => c.id === courseId);
        if (!course) {
          this.error = 'Курс не найден';
          this.currentLesson = null;
          this.currentCourse = null;
          this.isLoading = false;
          return;
        }
        const lesson = course.lessons?.find((l) => String(l.id) === String(lessonId));
        if (!lesson) {
          this.error = 'Урок не найден';
          this.currentLesson = null;
        } else {
          this.currentLesson = lesson;
        }
        this.currentCourse = {
          ...course,
          enrollment: this.getEnrollment(course.id),
        };
        this.isLoading = false;
      });
    }, 300);
  }

  async completeLesson(lessonId, score = null) {
    if (!this.currentCourse) {
      this.error = 'Курс не загружен';
      return false;
    }
    const courseId = this.currentCourse.id;
    const course = MOCK_COURSES.find((c) => c.id === courseId);
    const totalLessons = course?.lessons?.length || 1;

    const existing = this.progressByCourse[courseId] || {
      completedLessons: [],
      progressPercentage: 0,
    };

    const completedLessons = new Set(existing.completedLessons || []);
    completedLessons.add(lessonId);

    const progressPercentage = Math.round(
      (completedLessons.size / totalLessons) * 100
    );

    this.progressByCourse[courseId] = {
      ...existing,
      completedLessons: Array.from(completedLessons),
      progressPercentage,
    };

    this.saveProgressToStorage();

    // Обновляем enrollment для текущего курса и списка курсов
    this.currentCourse = {
      ...this.currentCourse,
      enrollment: this.getEnrollment(courseId),
    };
    this.courses = this.courses.map((c) =>
      c.id === courseId ? { ...c, enrollment: this.getEnrollment(courseId) } : c
    );

    return true;
  }
}

export const courseStore = new CourseStore();

