import React, { useEffect } from 'react';
import { Box, Grid, Card, CardContent, CardMedia, Typography, Button, CircularProgress, Alert } from '@mui/material';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { courseStore } from '../stores/CourseStore';

const CoursesPage = observer(() => {
  useEffect(() => {
    courseStore.loadCourses();
  }, []);

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

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Курсы
      </Typography>
      <Grid container spacing={4} sx={{ mt: 2 }}>
        {courseStore.courses.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              {course.thumbnail_url && (
                <CardMedia
                  component="img"
                  height="200"
                  image={course.thumbnail_url}
                  alt={course.title}
                />
              )}
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" component="h2" gutterBottom>
                  {course.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {course.description}
                </Typography>
                <Typography variant="body2" color="primary" gutterBottom>
                  Уровень: {course.difficulty === 'basic' ? 'Базовый' : 'Расширенный'}
                </Typography>
                <Button
                  component={Link}
                  to={`/courses/${course.id}`}
                  variant="contained"
                  fullWidth
                  sx={{ mt: 2, minHeight: '48px' }}
                >
                  Подробнее
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
});

export default CoursesPage;

