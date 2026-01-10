# Admin Panel Web

React frontend for the Admin Panel application.

## Tech Stack

- React 18
- Vite
- TypeScript
- TailwindCSS
- shadcn/ui components
- React Query
- React Router
- React Hook Form

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── layout/      # App layout components
│   ├── ui/          # shadcn/ui components
│   ├── projects/    # Project-specific components
│   └── users/       # User-specific components
├── contexts/        # React contexts (auth, theme)
├── hooks/           # Custom hooks
├── lib/             # Utilities (api, types, utils)
├── pages/           # Page components
└── main.tsx         # App entry point
```

## Pages

- `/login` - Login page
- `/` - Dashboard
- `/projects` - Projects management
- `/users` - Users management
- `/audit-logs` - Audit log viewer (admin only)
- `/settings` - User settings

## Environment Variables

| Variable       | Description     | Default |
|----------------|-----------------|---------|
| `VITE_API_URL` | Backend API URL | `/api`  |

## Build

```bash
npm run build
```

The build output will be in the `dist` folder.
