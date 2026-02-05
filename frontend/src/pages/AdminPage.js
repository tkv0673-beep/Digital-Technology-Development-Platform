import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { observer } from 'mobx-react-lite';

const AdminPage = observer(() => {
  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Админ панель
      </Typography>
      <Paper sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Управление курсами
        </Typography>
        <Button variant="contained" sx={{ mt: 2, minHeight: '56px' }}>
          Создать новый курс
        </Button>
        <Typography variant="body1" sx={{ mt: 4 }}>
          Здесь будет интерфейс для создания и управления курсами
        </Typography>
      </Paper>
    </Box>
  );
});

export default AdminPage;

