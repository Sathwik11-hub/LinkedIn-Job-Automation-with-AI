# AutoAgentHire React Frontend

A modern, beautiful React.js frontend for the AutoAgentHire LinkedIn job automation platform.

## Features

🎨 **Modern UI Design**
- Beautiful glassmorphism design with gradient backgrounds
- Smooth animations and transitions
- Responsive layout for all screen sizes
- Tailwind CSS for styling

🚀 **Interactive Components**
- Real-time automation progress tracking
- Drag & drop file upload
- Tabbed preference configuration
- Live status indicators

📊 **Results Display**
- Detailed job analysis cards
- Success metrics and statistics
- Interactive job matching scores
- Application status tracking

## Quick Start

1. **Install Dependencies**
   ```bash
   cd frontend/react
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Or use the startup script**
   ```bash
   ./start_react_frontend.sh
   ```

The React frontend will be available at: http://localhost:3000

## Project Structure

```
frontend/react/
├── app/
│   ├── layout.js          # Root layout component
│   ├── page.js            # Home page
│   └── globals.css        # Global styles
├── components/
│   └── AutoAgentHire.jsx  # Main application component
├── package.json           # Dependencies and scripts
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Backend Integration

The React frontend communicates with the FastAPI backend running on `http://127.0.0.1:8000`:

- **Health Check**: `GET /health`
- **Run Automation**: `POST /api/run-agent`
- **Agent Status**: `GET /api/agent/status`

## Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Language**: JavaScript/JSX
- **Package Manager**: npm

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Styling

The project uses Tailwind CSS with custom configurations:
- Glass morphism effects
- Custom animations
- Gradient backgrounds
- Responsive design utilities

## Deployment

To build for production:

```bash
npm run build
npm run start
```

## Features Overview

### Quick Start Section
- One-click automation with default settings
- Job title and location selection
- Instant AutoAgent launch

### Advanced Configuration
- Resume upload with drag & drop
- Tabbed preference settings
- Similarity threshold controls
- Auto-apply toggle

### Real-time Progress
- Animated progress bar
- Status text updates
- Cancel option
- Visual feedback

### Results Display
- Success/failure indicators
- Job metrics and statistics
- Individual job analysis cards
- Application status tracking

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the frontend
5. Submit a pull request

## License

This project is part of the AutoAgentHire system and follows the main project license.