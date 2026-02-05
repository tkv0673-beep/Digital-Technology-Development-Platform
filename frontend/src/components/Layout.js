import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';

const Layout = observer(({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    authStore.logout();
    navigate('/');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
            Платформа обучения
          </Typography>
          {authStore.isAuthenticated ? (
            <>
              <Button color="inherit" component={Link} to="/courses">
                Курсы
              </Button>
              <Button color="inherit" component={Link} to="/profile">
                Профиль
              </Button>
              {authStore.isMentor && (
                <Button color="inherit" component={Link} to="/admin">
                  Админ панель
                </Button>
              )}
              <Button color="inherit" onClick={handleLogout}>
                Выход
              </Button>
            </>
          ) : (
            <>
              <Button color="inherit" component={Link} to="/login">
                Вход
              </Button>
              <Button color="inherit" component={Link} to="/register">
                Регистрация
              </Button>
            </>
          )}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ flex: 1, py: 4 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ py: 3, mt: 'auto', bgcolor: 'grey.100', textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          © 2024 Платформа обучения цифровым технологиям
        </Typography>
      </Box>
    </Box>
  );
});

export default Layout;

