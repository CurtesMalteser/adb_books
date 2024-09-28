import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from '../features/home/Home';
import RouteLayout from '../pages/RootLayout';
import ErrorPage from '../pages/ErrorPage';
import BookDetails from '../features/bookDetails/BookDetails';
import MyBookList from '../features/booklist/MyBooklist';
import ROUTES from '../constants/Routes';
import RequireAuth from '../features/auth/RequireAuth';
import Login from '../features/auth/Login';
import CallbackPage from '../features/auth/CallbackPage';

const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <RouteLayout />,
    errorElement: <ErrorPage />,
    children: [
      { path: ROUTES.HOME, element: <RequireAuth><HomePage /></RequireAuth> },
      { path: ROUTES.MY_BOOKLIST, element: <RequireAuth><MyBookList /></RequireAuth> },
      {
        path: ROUTES.BOOK_DETAILS,
        element: <RequireAuth><BookDetails /></RequireAuth>,
      },
      { path: ROUTES.LOGIN, element: <Login /> },
      { path: ROUTES.LOGIN, element: <CallbackPage /> },
    ]
  },
])

function App() {

  return (
    <RouterProvider router={router} />
  )
}

export default App;
