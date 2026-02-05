import React, { useState } from 'react';
import { Box, Paper, TextField, Button, Typography, List, ListItem, ListItemText } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';
import { authStore } from '../stores/AuthStore';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const ChatBot = ({ lessonId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/chatbot/message/`,
        {
          message: input,
          lesson_id: lessonId,
        },
        {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        }
      );

      const botMessage = { role: 'bot', text: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { role: 'bot', text: 'Извините, произошла ошибка' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Виртуальный помощник
      </Typography>
      <Box sx={{ maxHeight: 400, overflowY: 'auto', mb: 2, minHeight: 200 }}>
        <List>
          {messages.map((msg, index) => (
            <ListItem
              key={index}
              sx={{
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  bgcolor: msg.role === 'user' ? 'primary.light' : 'grey.200',
                  maxWidth: '70%',
                }}
              >
                <ListItemText primary={msg.text} />
              </Paper>
            </ListItem>
          ))}
        </List>
      </Box>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          placeholder="Задайте вопрос..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          disabled={isLoading}
          sx={{ '& .MuiInputBase-input': { fontSize: '1.1rem' } }}
        />
        <Button
          variant="contained"
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          sx={{ minHeight: '56px', minWidth: '56px' }}
        >
          <SendIcon />
        </Button>
      </Box>
    </Paper>
  );
};

export default ChatBot;

