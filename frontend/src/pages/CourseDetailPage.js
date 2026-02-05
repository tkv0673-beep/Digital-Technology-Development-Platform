import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Box, Typography, Button, List, ListItem, ListItemText, CircularProgress, Alert, Paper } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { courseStore } from '../stores/CourseStore';

const CourseDetailPage = observer(() => {
  const { id } = useParams();

  useEffect(() => {
    courseStore.loadCourse(id);
  }, [id]);

  const handleEnroll = async () => {
    await courseStore.enrollInCourse(id);
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

  const course = courseStore.currentCourse;
  if (!course) return null;

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        {course.title}
      </Typography>
      <Typography variant="body1" paragraph>
        {course.description}
      </Typography>
      {!course.enrollment && (
        <Button
          variant="contained"
          size="large"
          onClick={handleEnroll}
          sx={{ mb: 4, minHeight: '56px', fontSize: '1.1rem' }}
        >
          Записаться на курс
        </Button>
      )}
      {course.enrollment && (
        <Paper sx={{ p: 2, mb: 4, bgcolor: 'success.light' }}>
          <Typography variant="body1">
            Прогресс: {course.enrollment.progress_percentage}%
          </Typography>
        </Paper>
      )}
      <Typography variant="h4" gutterBottom sx={{ mt: 4 }}>
        Уроки
      </Typography>
      <List>
        {course.lessons?.map((lesson, index) => (
          <ListItem
            key={lesson.id}
            component={Link}
            to={`/courses/${id}/lessons/${lesson.id}`}
            sx={{
              textDecoration: 'none',
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
              mb: 1,
              '&:hover': { bgcolor: 'action.hover' },
            }}
          >
            <ListItemText
              primary={`Урок ${index + 1}: ${lesson.title}`}
              secondary={lesson.description}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
});

export default CourseDetailPage;

