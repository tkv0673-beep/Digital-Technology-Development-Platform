import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';

const ProfilePage = observer(() => {
  const user = authStore.user;
  if (!user) return null;

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
              Статистика
            </Typography>
            <Typography variant="body1">
              Здесь будет статистика прохождения курсов
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
});

export default ProfilePage;

