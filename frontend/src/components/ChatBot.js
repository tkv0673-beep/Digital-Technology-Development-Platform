import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

// Мок-подсказки в зависимости от урока и шага
const ASSISTANT_HINTS = {
  'smartphone-basic-lesson': [
    'Чтобы включить смартфон, найдите кнопку питания сбоку корпуса и нажмите её.',
    'Для увеличения громкости используйте верхнюю кнопку громкости.',
    'Для уменьшения громкости нажмите нижнюю кнопку громкости.',
    'Чтобы выключить смартфон, зажмите кнопку питания чуть дольше.',
  ],
  'smartphone-advanced-lesson': [
    'Откройте «Настройки», иконка обычно выглядит как шестерёнка.',
    'В настройках найдите раздел «Wi‑Fi».',
    'Выберите нужную сеть из списка.',
    'Аккуратно введите пароль от сети и подтвердите.',
    'Найдите иконку RuStore на экране смартфона.',
    'Воспользуйтесь строкой поиска, чтобы найти приложение.',
    'Нажмите кнопку «Установить» рядом с приложением.',
  ],
  'messenger-basic-lesson': [
    'Откройте приложение MAX с главного экрана.',
    'Нажмите на кнопку «Новый чат», чтобы создать чат.',
    'Используйте поиск, чтобы найти нужный контакт.',
    'Выберите контакт из списка, чтобы открыть чат.',
    'Введите приветственное сообщение в поле ввода внизу экрана.',
    'Нажмите на иконку вложений или фото, чтобы отправить изображение.',
  ],
  'messenger-advanced-lesson': [
    'Найдите кнопку «Новая группа» в списке чатов.',
    'Отметьте несколько контактов для добавления в группу.',
    'Подтвердите создание группы кнопкой «Создать».',
    'Откройте панель эмодзи и выберите смайлик.',
    'Переключитесь на вкладку стикеров и выберите подходящий стикер.',
  ],
  'shopping-basic-lesson': [
    'Сначала откройте раздел «Каталог» в магазине.',
    'Введите название товара в строку поиска.',
    'Нажмите на нужный товар в списке результатов.',
    'Нажмите кнопку «В корзину», чтобы добавить товар.',
  ],
  'shopping-advanced-lesson': [
    'Откройте корзину, нажав на иконку в правом верхнем углу.',
    'Выберите удобный способ доставки: курьер или пункт выдачи.',
    'Выберите или введите адрес доставки.',
    'Выберите способ оплаты: карта, СБП или при получении.',
    'Проверьте данные и нажмите кнопку оформления заказа.',
  ],
  'gosuslugi-basic-lesson': [
    'Откройте портал, нажав на кнопку «Госуслуги».',
    'Введите номер телефона, почту или СНИЛС в поле логина.',
    'Введите пароль и нажмите «Войти».',
    'Найдите услугу «Запись к врачу».',
    'Введите номер полиса ОМС.',
    'Выберите специальность (например, терапевт).',
    'Выберите конкретного врача.',
    'Укажите поликлинику.',
    'Выберите удобные дату и время.',
    'Нажмите кнопку подтверждения записи.',
  ],
  'gosuslugi-advanced-lesson': [
    'Откройте «Каталог услуг» на портале.',
    'Воспользуйтесь поиском и введите «пенсионное удостоверение».',
    'Выберите услугу «Электронное свидетельство пенсионера».',
    'Аккуратно заполните все обязательные поля заявления.',
    'Нажмите кнопку «Отправить» для отправки заявления.',
  ],
};

const ChatBot = ({ lessonId, currentStepIndex = 0 }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const getContextHint = () => {
    const hints = ASSISTANT_HINTS[lessonId];
    if (!hints || hints.length === 0) {
      return 'Следуйте подсказкам рядом с тренажёром и двигайтесь по шагам сверху вниз.';
    }
    const index = Math.min(currentStepIndex, hints.length - 1);
    return hints[index];
  };

  const pushBotMessage = (text) => {
    const botMessage = { role: 'bot', text };
    setMessages((prev) => [...prev, botMessage]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Мок-логика: отвечаем с учётом текущего шага урока
    const baseHint = getContextHint();
    const botText = `Я виртуальный помощник. Сейчас мы тренируемся по уроку "${lessonId}".\n\nПодсказка по текущему шагу:\n${baseHint}`;
    pushBotMessage(botText);
    setIsLoading(false);
  };

  const handleHelpClick = () => {
    const hint = getContextHint();
    pushBotMessage(`Подсказка по текущему шагу:\n${hint}`);
  };

  return (
    <Paper sx={{ p: 3, mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Виртуальный помощник
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Задавайте вопросы или нажмите кнопку «Подсказка по шагу», чтобы получить совет, что
        делать дальше.
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
      <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
        <Button
          variant="outlined"
          onClick={handleHelpClick}
          disabled={isLoading}
          sx={{ minHeight: '40px' }}
        >
          Подсказка по шагу
        </Button>
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

