import { useEffect } from 'react';
import BooksList from '../../components/books/BooksList';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import {
  fetchBooklistAsync,
  Shelves,
  shelvesAreEmptySelector,
  shelvesSelector,
  statusSelector,
} from './myBooklistSlice';
import { Status } from '../../constants/Status';
import { Card, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import ROUTES from '../../constants/Routes';
import Loader from '../loader/Loader';

const MyBooklistContent: React.FC<Shelves> = ({ read, wantToRead, currentlyReading }) => {
  return (
    <BooksList
      readBooks={read}
      wantToRead={wantToRead}
      currentlyReading={currentlyReading} />
  )
}

const MyBooklistEmpty: React.FC = () => {
  return (
    <Container style={{ marginTop: 20, marginBottom: 20, }}>
      <Card border="primary">
        <Card.Body>
          <Card.Title>Your bookshelves are empty</Card.Title>
          <Card.Text>
            Start adding books to your shelves by searching for them.
          </Card.Text>
          <Card.Link as={Link} to={ROUTES.HOME}>Home</Card.Link>
        </Card.Body>
      </Card>
    </Container>
  )
}

function MyBooklist() {

  const dispatch = useAppDispatch()
  const status = useAppSelector(statusSelector);
  const shelves = useAppSelector(shelvesSelector);
  const shelvesAreEmpty = useAppSelector(shelvesAreEmptySelector);

  useEffect(() => {
    dispatch(fetchBooklistAsync())
  }, [dispatch])


  return (
    <>
      {status === Status.LOADING && <Loader />}
      {status === Status.IDLE && (shelvesAreEmpty ? <MyBooklistEmpty /> : <MyBooklistContent {...shelves} />)}
      {status === Status.FAILED && <h1>Error...</h1>}
    </>
  );

}

export default MyBooklist;
