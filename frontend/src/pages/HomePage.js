import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';

const HomePage = observer(() => {
  return (
    <Container>
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h1" component="h1" gutterBottom>
          Добро пожаловать на платформу обучения!
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Освойте цифровые технологии в безопасной и дружелюбной среде
        </Typography>
        {!authStore.isAuthenticated ? (
          <Box sx={{ mt: 4 }}>
            <Button
              variant="contained"
              size="large"
              component={Link}
              to="/register"
              sx={{ mr: 2, minHeight: '56px', fontSize: '1.2rem', px: 4 }}
            >
              Начать обучение
            </Button>
            <Button
              variant="outlined"
              size="large"
              component={Link}
              to="/login"
              sx={{ minHeight: '56px', fontSize: '1.2rem', px: 4 }}
            >
              Войти
            </Button>
          </Box>
        ) : (
          <Box sx={{ mt: 4 }}>
            <Button
              variant="contained"
              size="large"
              component={Link}
              to="/courses"
              sx={{ minHeight: '56px', fontSize: '1.2rem', px: 4 }}
            >
              Перейти к курсам
            </Button>
          </Box>
        )}
      </Box>
    </Container>
  );
});

export default HomePage;

