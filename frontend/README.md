# Frontend - React Application

React приложение с архитектурой MVVM для платформы обучения.

## Установка

```bash
npm install
```

## Запуск

```bash
npm start
```

Приложение будет доступно по адресу http://localhost:3000

## Сборка

```bash
npm run build
```

## Тестирование

```bash
npm test
```

## Структура

- `src/stores/` - MobX stores (ViewModel)
- `src/pages/` - Страницы приложения
- `src/components/` - Переиспользуемые компоненты
- `src/utils/` - Утилиты и хелперы

## Архитектура MVVM

- **Model**: API endpoints и данные
- **View**: React компоненты
- **ViewModel**: MobX stores для управления состоянием

