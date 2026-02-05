import { useEffect } from 'react';
import { courseStore } from '../stores/CourseStore';

export const useCourse = (courseId) => {
  useEffect(() => {
    if (courseId) {
      courseStore.loadCourse(courseId);
    }
  }, [courseId]);

  return {
    course: courseStore.currentCourse,
    isLoading: courseStore.isLoading,
    error: courseStore.error,
  };
};

export default useCourse;

