import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from '../features/home/Home';
import RouteLayout from '../pages/RootLayout';
import ErrorPage from '../pages/ErrorPage';
import BookDetails from '../features/bookDetails/BookDetails';
import MyBookList from '../features/booklist/MyBooklist';
import ROUTES from '../constants/Routes';


const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <RouteLayout />,
    errorElement: <ErrorPage />,
    children: [
      { path: ROUTES.HOME, element: <HomePage /> },
      { path: ROUTES.MY_BOOKLIST, element: <MyBookList /> },
      {
        path: ROUTES.BOOK_DETAILS,
        element: <BookDetails />,
      },
    ]
  },
])

function App() {
  return (
    <RouterProvider router={router} />
  )
}

export default App;
