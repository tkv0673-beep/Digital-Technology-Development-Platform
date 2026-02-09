import React from 'react';
import { Box, Typography, Paper, Grid, List, ListItem, ListItemText } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';
import { courseStore } from '../stores/CourseStore';

const ProfilePage = observer(() => {
  const user = authStore.user;
  if (!user) return null;

  const progressEntries = Object.entries(courseStore.progressByCourse || {});
  const totalCompletedCourses = progressEntries.filter(
    ([, value]) => (value.progressPercentage || 0) >= 100
  ).length;
  const totalInProgress = progressEntries.filter(
    ([, value]) => (value.progressPercentage || 0) > 0 && (value.progressPercentage || 0) < 100
  ).length;

  const achievements = [];
  if (progressEntries.length > 0) {
    achievements.push('Сделан первый шаг в цифровом тренажёре');
  }
  if (totalCompletedCourses >= 1) {
    achievements.push('Пройден первый курс');
  }
  if (totalCompletedCourses >= 3) {
    achievements.push('Уверенный пользователь цифровых сервисов');
  }

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Профиль
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Личная информация
            </Typography>
            <Typography variant="body1">
              <strong>Имя пользователя:</strong> {user.username}
            </Typography>
            <Typography variant="body1">
              <strong>Email:</strong> {user.email}
            </Typography>
            <Typography variant="body1">
              <strong>Роль:</strong> {user.role === 'mentor' ? 'Ментор' : 'Менти'}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Статистика по курсам
            </Typography>
            {progressEntries.length === 0 && (
              <Typography variant="body1">
                Вы ещё не начали прохождение курсов. Откройте раздел «Курсы», чтобы начать обучение.
              </Typography>
            )}
            {progressEntries.length > 0 && (
              <>
                <Typography variant="body1" gutterBottom>
                  Всего курсов с прогрессом: {progressEntries.length}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Завершённых курсов: {totalCompletedCourses}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Курсов в процессе: {totalInProgress}
                </Typography>
                <List dense>
                  {progressEntries.map(([courseId, value]) => (
                    <ListItem key={courseId}>
                      <ListItemText
                        primary={courseId}
                        secondary={`Прогресс: ${value.progressPercentage || 0}%`}
                      />
                    </ListItem>
                  ))}
                </List>
              </>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Достижения
            </Typography>
            {achievements.length === 0 ? (
              <Typography variant="body1">
                Выполняйте шаги в курсах, чтобы открывать достижения.
              </Typography>
            ) : (
              <List dense>
                {achievements.map((a) => (
                  <ListItem key={a}>
                    <ListItemText primary={a} />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
});

export default ProfilePage;

