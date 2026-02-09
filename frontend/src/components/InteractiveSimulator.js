import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Stack,
  RadioGroup,
  FormControlLabel,
  Radio,
  Alert,
} from '@mui/material';

// Координаты "курсора" для имитации движения по экрану
const CURSOR_POSITIONS = {
  smartphone: {
    power: { top: '12%', left: '88%' },
    'volume-up': { top: '30%', left: '8%' },
    'volume-down': { top: '45%', left: '8%' },
  },
  'smartphone-wifi': {
    settings: { top: '18%', left: '50%' },
    wifi: { top: '30%', left: '50%' },
    network: { top: '45%', left: '50%' },
    password: { top: '60%', left: '50%' },
    rustore: { top: '78%', left: '30%' },
    search: { top: '18%', left: '50%' },
    install: { top: '60%', left: '50%' },
  },
  messenger: {
    'open-max': { top: '78%', left: '20%' },
    'new-chat': { top: '15%', left: '90%' },
    'search-contact': { top: '24%', left: '50%' },
    contact: { top: '40%', left: '50%' },
    'input-text': { top: '88%', left: '60%' },
    'attach-photo': { top: '88%', left: '20%' },
  },
  'messenger-group': {
    'new-group': { top: '15%', left: '80%' },
    'select-members': { top: '40%', left: '50%' },
    'confirm-group': { top: '18%', left: '15%' },
    emoji: { top: '88%', left: '20%' },
    sticker: { top: '88%', left: '35%' },
  },
  shopping: {
    catalog: { top: '18%', left: '15%' },
    'search-item': { top: '18%', left: '60%' },
    'open-item': { top: '40%', left: '50%' },
    'add-to-cart': { top: '70%', left: '50%' },
  },
  'shopping-checkout': {
    cart: { top: '10%', left: '90%' },
    delivery: { top: '40%', left: '30%' },
    address: { top: '50%', left: '30%' },
    payment: { top: '60%', left: '30%' },
    'confirm-order': { top: '80%', left: '50%' },
  },
  gosuslugi: {
    'gosuslugi-button': { top: '20%', left: '50%' },
    login: { top: '35%', left: '50%' },
    password: { top: '45%', left: '50%' },
    'med-service': { top: '60%', left: '50%' },
    policy: { top: '35%', left: '30%' },
    speciality: { top: '50%', left: '30%' },
    doctor: { top: '60%', left: '30%' },
    clinic: { top: '70%', left: '30%' },
    time: { top: '80%', left: '50%' },
    confirm: { top: '88%', left: '50%' },
  },
  'gosuslugi-pension': {
    services: { top: '25%', left: '40%' },
    'search-service': { top: '25%', left: '75%' },
    'open-service': { top: '40%', left: '50%' },
    form: { top: '55%', left: '50%' },
    send: { top: '80%', left: '50%' },
  },
};

const getCursorPosition = (simulationType, elementId) => {
  return (
    CURSOR_POSITIONS[simulationType]?.[elementId] || {
      top: '50%',
      left: '50%',
    }
  );
};

const InteractiveSimulator = ({ lesson, onReadyToComplete, onStepChange }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [cursorPosition, setCursorPosition] = useState({ top: '50%', left: '50%' });
  const [isTestPhase, setIsTestPhase] = useState(false);
  const [selectedOptionId, setSelectedOptionId] = useState(null);
  const [testChecked, setTestChecked] = useState(false);
  const [testCorrect, setTestCorrect] = useState(false);

  const hasTest = Array.isArray(lesson.tests) && lesson.tests.length > 0;
  const currentStep = !isTestPhase ? lesson.steps[currentStepIndex] : null;
  const currentTest = hasTest ? lesson.tests[0] : null;

  useEffect(() => {
    // При смене урока сбрасываем состояние
    setCurrentStepIndex(0);
    setStatusMessage('');
    setErrorMessage('');
    setIsTestPhase(false);
    setSelectedOptionId(null);
    setTestChecked(false);
    setTestCorrect(false);
    setCursorPosition({ top: '50%', left: '50%' });
    if (onStepChange) {
      onStepChange(0);
    }
  }, [lesson, onStepChange]);

  const handleElementClick = (elementId) => {
    if (isTestPhase || !currentStep) return;

    if (elementId === currentStep.targetElementId) {
      setErrorMessage('');
      setStatusMessage(currentStep.successMessage || 'Шаг выполнен верно!');

      const nextIndex = currentStepIndex + 1;
      if (nextIndex < lesson.steps.length) {
        setTimeout(() => {
          setCurrentStepIndex(nextIndex);
          setStatusMessage('');
          if (onStepChange) {
            onStepChange(nextIndex);
          }
        }, 600);
      } else if (hasTest) {
        // Переход к тесту
        setTimeout(() => {
          setIsTestPhase(true);
          if (onStepChange) {
            onStepChange(lesson.steps.length); // условный индекс "теста"
          }
        }, 600);
      } else {
        // Урок можно завершать
        if (onReadyToComplete) {
          onReadyToComplete();
        }
      }
    } else {
      setStatusMessage('');
      setErrorMessage('Это не та область. Попробуйте ещё раз или нажмите «Подсказка».');
    }
  };

  const handleShowHint = () => {
    if (!currentStep) return;
    const pos = getCursorPosition(lesson.simulationType, currentStep.targetElementId);
    setCursorPosition(pos);
    setStatusMessage(currentStep.hint || 'Обратите внимание на подсвеченную область.');
    setErrorMessage('');
  };

  const handleCheckTest = () => {
    if (!currentTest || !selectedOptionId) return;
    const correct = selectedOptionId === currentTest.correctOptionId;
    setTestChecked(true);
    setTestCorrect(correct);
    if (correct) {
      setStatusMessage(
        currentTest.explanation || 'Тест пройден успешно! Можно переходить к следующему уроку.'
      );
      setErrorMessage('');
      if (onReadyToComplete) {
        onReadyToComplete();
      }
    } else {
      setErrorMessage('Ответ неверный. Попробуйте ещё раз.');
      setStatusMessage('');
    }
  };

  const renderPhoneFrame = (content) => (
    <Box
      sx={{
        position: 'relative',
        maxWidth: 360,
        mx: 'auto',
        height: 640,
        borderRadius: 6,
        border: '4px solid #212121',
        bgcolor: '#fafafa',
        boxShadow: 4,
        overflow: 'hidden',
      }}
    >
      <Box
        sx={{
          height: 32,
          bgcolor: '#1976d2',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 14,
        }}
      >
        Тренажёр интерфейса
      </Box>
      <Box sx={{ p: 2, height: 'calc(100% - 32px)' }}>{content}</Box>
      {/* Анимированный "курсор" */}
      <Box
        sx={{
          position: 'absolute',
          width: 24,
          height: 24,
          borderRadius: '50%',
          border: '3px solid #ff9800',
          boxShadow: '0 0 8px rgba(255,152,0,0.7)',
          transition: 'top 0.5s ease, left 0.5s ease',
          pointerEvents: 'none',
          top: cursorPosition.top,
          left: cursorPosition.left,
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
        }}
      />
    </Box>
  );

  const renderClickableButton = (id, label, activeId) => (
    <Button
      onClick={() => handleElementClick(id)}
      variant={id === activeId ? 'contained' : 'outlined'}
      color={id === activeId ? 'secondary' : 'primary'}
      sx={{
        minHeight: 48,
        fontSize: '0.9rem',
        borderStyle: id === activeId ? 'solid' : 'dashed',
      }}
    >
      {label}
    </Button>
  );

  const renderSimulationContent = () => {
    const activeId = currentStep?.targetElementId || '';

    switch (lesson.simulationType) {
      case 'smartphone':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Экран смартфона
            </Typography>
            <Stack direction="row" justifyContent="space-between">
              {renderClickableButton('power', 'Кнопка питания', activeId)}
            </Stack>
            <Stack direction="row" spacing={2} sx={{ mt: 4 }}>
              {renderClickableButton('volume-up', 'Громкость +', activeId)}
              {renderClickableButton('volume-down', 'Громкость −', activeId)}
            </Stack>
            <Box sx={{ flexGrow: 1 }} />
            <Typography variant="body2" color="text.secondary">
              Нажмите на нужную кнопку, чтобы выполнить шаг безопасно.
            </Typography>
          </Stack>
        );
      case 'smartphone-wifi':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Настройки смартфона и RuStore
            </Typography>
            {renderClickableButton('settings', 'Настройки', activeId)}
            {renderClickableButton('wifi', 'Wi‑Fi', activeId)}
            {renderClickableButton('network', 'Сеть «Домашний Wi‑Fi»', activeId)}
            {renderClickableButton('password', 'Поле ввода пароля', activeId)}
            <Box sx={{ mt: 2 }} />
            {renderClickableButton('rustore', 'RuStore', activeId)}
            {renderClickableButton('search', 'Строка поиска', activeId)}
            {renderClickableButton('install', 'Кнопка «Установить»', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'messenger':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Мессенджер MAX
            </Typography>
            {renderClickableButton('open-max', 'Открыть MAX', activeId)}
            {renderClickableButton('new-chat', 'Новый чат', activeId)}
            {renderClickableButton('search-contact', 'Поиск контакта', activeId)}
            {renderClickableButton('contact', 'Контакт «Иван Иванов»', activeId)}
            {renderClickableButton('input-text', 'Строка ввода сообщения', activeId)}
            {renderClickableButton('attach-photo', 'Кнопка отправки фото', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'messenger-group':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Групповой чат MAX
            </Typography>
            {renderClickableButton('new-group', 'Новая группа', activeId)}
            {renderClickableButton('select-members', 'Выбор участников', activeId)}
            {renderClickableButton('confirm-group', 'Создать группу', activeId)}
            {renderClickableButton('emoji', 'Кнопка эмодзи', activeId)}
            {renderClickableButton('sticker', 'Кнопка стикеров', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'shopping':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Интернет‑магазин
            </Typography>
            {renderClickableButton('catalog', 'Раздел «Каталог»', activeId)}
            {renderClickableButton('search-item', 'Строка поиска товара', activeId)}
            {renderClickableButton('open-item', 'Карточка товара', activeId)}
            {renderClickableButton('add-to-cart', 'Кнопка «В корзину»', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'shopping-checkout':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Оформление заказа
            </Typography>
            {renderClickableButton('cart', 'Корзина', activeId)}
            {renderClickableButton('delivery', 'Способ доставки', activeId)}
            {renderClickableButton('address', 'Адрес доставки', activeId)}
            {renderClickableButton('payment', 'Способ оплаты', activeId)}
            {renderClickableButton('confirm-order', 'Оформить заказ', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'gosuslugi':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Портал Госуслуг — запись к врачу
            </Typography>
            {renderClickableButton('gosuslugi-button', 'Кнопка «Госуслуги»', activeId)}
            {renderClickableButton('login', 'Поле логина', activeId)}
            {renderClickableButton('password', 'Поле пароля', activeId)}
            {renderClickableButton('med-service', 'Услуга «Запись к врачу»', activeId)}
            {renderClickableButton('policy', 'Поле номера полиса', activeId)}
            {renderClickableButton('speciality', 'Выбор специальности', activeId)}
            {renderClickableButton('doctor', 'Выбор врача', activeId)}
            {renderClickableButton('clinic', 'Выбор поликлиники', activeId)}
            {renderClickableButton('time', 'Выбор даты и времени', activeId)}
            {renderClickableButton('confirm', 'Подтвердить запись', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      case 'gosuslugi-pension':
        return (
          <Stack spacing={2} sx={{ height: '100%' }}>
            <Typography variant="subtitle1" gutterBottom>
              Госуслуги — электронное свидетельство пенсионера
            </Typography>
            {renderClickableButton('services', 'Каталог услуг', activeId)}
            {renderClickableButton('search-service', 'Поиск услуги', activeId)}
            {renderClickableButton('open-service', 'Открыть услугу', activeId)}
            {renderClickableButton('form', 'Форма заявления', activeId)}
            {renderClickableButton('send', 'Отправить заявление', activeId)}
            <Box sx={{ flexGrow: 1 }} />
          </Stack>
        );
      default:
        return (
          <Typography variant="body2" color="text.secondary">
            Для этого урока пока нет отдельного визуального тренажёра.
          </Typography>
        );
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Интерактивная симуляция
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Вы находитесь в безопасной обучающей среде. Нажимайте на подсвеченные области, чтобы
        по шагам выполнить сценарий из реального интерфейса.
      </Typography>

      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          gap: 3,
        }}
      >
        {renderPhoneFrame(renderSimulationContent())}

        <Box sx={{ flex: 1, minWidth: 0 }}>
          {!isTestPhase && currentStep && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Шаг {currentStepIndex + 1} из {lesson.steps.length}
              </Typography>
              <Typography variant="h6" gutterBottom>
                {currentStep.title}
              </Typography>
              <Typography variant="body1" paragraph>
                {currentStep.description}
              </Typography>
              <Stack direction="row" spacing={2} sx={{ mt: 1 }}>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={handleShowHint}
                  sx={{ minHeight: 48 }}
                >
                  Подсказка (показать курсор)
                </Button>
              </Stack>
            </Box>
          )}

          {isTestPhase && currentTest && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Проверка усвоения материала
              </Typography>
              <Typography variant="h6" gutterBottom>
                {currentTest.question}
              </Typography>
              <RadioGroup
                value={selectedOptionId}
                onChange={(e) => {
                  setSelectedOptionId(e.target.value);
                  setTestChecked(false);
                  setTestCorrect(false);
                  setErrorMessage('');
                  setStatusMessage('');
                }}
              >
                {currentTest.options.map((opt) => (
                  <FormControlLabel
                    key={opt.id}
                    value={opt.id}
                    control={<Radio />}
                    label={opt.text}
                  />
                ))}
              </RadioGroup>
              <Button
                variant="contained"
                sx={{ mt: 2, minHeight: 48 }}
                disabled={!selectedOptionId}
                onClick={handleCheckTest}
              >
                Проверить ответ
              </Button>
              {testChecked && (
                <Box sx={{ mt: 2 }}>
                  {testCorrect ? (
                    <Alert severity="success">
                      Отлично! Вы правильно ответили на вопрос.{' '}
                      {currentTest.explanation && <span>{currentTest.explanation}</span>}
                    </Alert>
                  ) : (
                    <Alert severity="warning">{errorMessage}</Alert>
                  )}
                </Box>
              )}
            </Box>
          )}

          {statusMessage && !isTestPhase && (
            <Alert severity="success" sx={{ mt: 1 }}>
              {statusMessage}
            </Alert>
          )}
          {errorMessage && !isTestPhase && (
            <Alert severity="warning" sx={{ mt: 1 }}>
              {errorMessage}
            </Alert>
          )}
        </Box>
      </Box>
    </Paper>
  );
};

export default InteractiveSimulator;

