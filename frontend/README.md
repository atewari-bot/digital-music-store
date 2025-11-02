# Digital Music Store Frontend

React + TypeScript frontend for the Digital Music Store AI Agent.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

## Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Configuration

Create a `.env` file to configure the API URL:

```bash
VITE_API_URL=http://localhost:8000
```

By default, it will use `http://localhost:8000` which is the default FastAPI server port.

