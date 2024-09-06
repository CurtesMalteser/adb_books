import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from '../features/home/Home';
import RouteLayout from '../pages/RootLayout';
import ErrorPage from '../pages/ErrorPage';
import BookDetails from '../pages/BookDetails';
import { loader as bookLoader } from '../pages/BookDetails';
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
        loader: bookLoader
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
