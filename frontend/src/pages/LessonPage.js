import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Paper, CircularProgress, Alert } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { courseStore } from '../stores/CourseStore';
import ChatBot from '../components/ChatBot';

const LessonPage = observer(() => {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    courseStore.loadLesson(courseId, lessonId);
  }, [courseId, lessonId]);

  const handleComplete = async () => {
    const success = await courseStore.completeLesson(lessonId);
    if (success) {
      navigate(`/courses/${courseId}`);
    }
  };

  if (courseStore.isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (courseStore.error) {
    return (
      <Alert severity="error" sx={{ mt: 4 }}>
        {courseStore.error}
      </Alert>
    );
  }

  const lesson = courseStore.currentLesson;
  if (!lesson) return null;

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        {lesson.title}
      </Typography>
      <Typography variant="body1" paragraph>
        {lesson.description}
      </Typography>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Интерактивная симуляция
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Здесь будет интерактивная симуляция интерфейса
        </Typography>
      </Paper>
      <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          onClick={handleComplete}
          sx={{ minHeight: '56px', fontSize: '1.1rem' }}
        >
          Завершить урок
        </Button>
        <Button
          variant="outlined"
          size="large"
          onClick={() => navigate(`/courses/${courseId}`)}
          sx={{ minHeight: '56px', fontSize: '1.1rem' }}
        >
          Назад к курсу
        </Button>
      </Box>
      <ChatBot lessonId={lessonId} />
    </Box>
  );
});

export default LessonPage;

