import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, CircularProgress, Alert } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { courseStore } from '../stores/CourseStore';
import ChatBot from '../components/ChatBot';
import InteractiveSimulator from '../components/InteractiveSimulator';

const LessonPage = observer(() => {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  const [isReadyToComplete, setIsReadyToComplete] = useState(false);
  const [showAssistant, setShowAssistant] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    courseStore.loadLesson(courseId, lessonId);
  }, [courseId, lessonId]);

  const handleComplete = async () => {
    if (!isReadyToComplete) return;
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
      <InteractiveSimulator
        lesson={lesson}
        onReadyToComplete={() => setIsReadyToComplete(true)}
        onStepChange={setCurrentStepIndex}
      />
      <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          onClick={handleComplete}
          sx={{ minHeight: '56px', fontSize: '1.1rem' }}
          disabled={!isReadyToComplete}
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
      <Box sx={{ mb: 2 }}>
        <Button
          variant="outlined"
          size="large"
          sx={{ minHeight: '56px', fontSize: '1.1rem' }}
          onClick={() => setShowAssistant((prev) => !prev)}
        >
          {showAssistant ? 'Скрыть помощника' : 'Помощь'}
        </Button>
      </Box>
      {showAssistant && (
        <ChatBot lessonId={lessonId} currentStepIndex={currentStepIndex} />
      )}
    </Box>
  );
});

export default LessonPage;

