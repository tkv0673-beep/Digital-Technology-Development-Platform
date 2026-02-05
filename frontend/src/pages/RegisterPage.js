import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Alert, MenuItem } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';

const RegisterPage = observer(() => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    phone: '',
    role: 'mentee',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password_confirm) {
      authStore.error = 'Пароли не совпадают';
      return;
    }
    const success = await authStore.register(formData);
    if (success) {
      navigate('/courses');
    }
  };

  return (
    <Box sx={{ maxWidth: 500, mx: 'auto', mt: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Регистрация
        </Typography>
        {authStore.error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {typeof authStore.error === 'object' ? JSON.stringify(authStore.error) : authStore.error}
          </Alert>
        )}
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Имя пользователя"
            name="username"
            value={formData.username}
            onChange={handleChange}
            margin="normal"
            required
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
            required
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            label="Имя"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            margin="normal"
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            label="Фамилия"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            margin="normal"
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            label="Телефон"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            margin="normal"
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            select
            label="Роль"
            name="role"
            value={formData.role}
            onChange={handleChange}
            margin="normal"
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          >
            <MenuItem value="mentee">Менти (ученик)</MenuItem>
            <MenuItem value="mentor">Ментор (преподаватель)</MenuItem>
          </TextField>
          <TextField
            fullWidth
            label="Пароль"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            required
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <TextField
            fullWidth
            label="Подтверждение пароля"
            name="password_confirm"
            type="password"
            value={formData.password_confirm}
            onChange={handleChange}
            margin="normal"
            required
            sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            sx={{ mt: 3, minHeight: '56px', fontSize: '1.1rem' }}
            disabled={authStore.isLoading}
          >
            {authStore.isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
          </Button>
        </form>
      </Paper>
    </Box>
  );
});

export default RegisterPage;

