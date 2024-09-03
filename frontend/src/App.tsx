import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/Home';
import RouteLayout from './pages/RootLayout';
import ErrorPage from './pages/ErrorPage';
import BookDetails from './pages/BookDetails';
import { loader as bookLoader } from './pages/BookDetails';
import BookSearch from './pages/BookSearch';
import BookShelfContextProvider from './store/BookShelfContext';


const router = createBrowserRouter([
  {
    path: '/',
    element: <RouteLayout />,
    errorElement: <ErrorPage />,
    children: [
      { path: '/', element: <HomePage /> },
      {
        path: '/book/:id',
        element: <BookDetails />,
        loader: bookLoader
      },
      {
        path: '/search',
        element: <BookSearch />
      }
    ]
  },
])

function App() {
  return (
    <BookShelfContextProvider>
      <RouterProvider router={router} />
    </BookShelfContextProvider>
  )
}

export default App;
