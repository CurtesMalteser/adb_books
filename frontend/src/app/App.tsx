import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from '../features/home/Home';
import Auth0ProviderLayout from '../pages/Auth0ProviderLayout';
import ErrorPage from '../pages/ErrorPage';
import BookDetails from '../features/bookDetails/BookDetails';
import MyBookList from '../features/booklist/MyBooklist';
import ROUTES from '../constants/Routes';
import RequireAuth from '../features/auth/RequireAuth';
import Login from '../features/auth/Login';
import CallbackPage from '../features/auth/CallbackPage';
import Profile from '../features/Profile';

const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <Auth0ProviderLayout />,
    errorElement: <ErrorPage />,
    children: [
      { path: ROUTES.HOME, element: <RequireAuth><HomePage /></RequireAuth> },
      { path: ROUTES.MY_BOOKLIST, element: <RequireAuth><MyBookList /></RequireAuth> },
      {
        path: ROUTES.BOOK_DETAILS,
        element: <RequireAuth><BookDetails /></RequireAuth>,
      },
      { path: ROUTES.LOGIN, element: <Login /> },
      { path: ROUTES.LOGIN_CALLBACK, element: <CallbackPage /> },
      { path: ROUTES.PROFILE, element: <RequireAuth><Profile /></RequireAuth> },
    ]
  },
])

function App() {
  return (
    <RouterProvider router={router} />
  )
}

export default App;
