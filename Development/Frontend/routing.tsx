import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './auth-provider';

// Protected Route Component
function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

// Public Route Component (redirect if authenticated)
function PublicRoute({ children }: { children: JSX.Element }) {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

// App Router
export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          }
        />

        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

// Page Components (placeholders)
function HomePage() {
  return <div><h1>Home Page</h1></div>;
}

function AboutPage() {
  return <div><h1>About Page</h1></div>;
}

function LoginPage() {
  return <div><h1>Login Page</h1></div>;
}

function RegisterPage() {
  return <div><h1>Register Page</h1></div>;
}

function DashboardPage() {
  return <div><h1>Dashboard</h1></div>;
}

function ProfilePage() {
  return <div><h1>Profile</h1></div>;
}

function SettingsPage() {
  return <div><h1>Settings</h1></div>;
}

function NotFoundPage() {
  return <div><h1>404 - Page Not Found</h1></div>;
}
