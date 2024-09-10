import { useEffect } from 'react';
import BooksList from '../../components/books/BooksList';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { fetchBooklistAsync, shelvesSelector, statusSelector } from './myBooklistSlice';
import { Status } from '../../constants/Status';

function MyBooklist() {

  const dispatch = useAppDispatch()
  const status = useAppSelector(statusSelector);
  const shelves = useAppSelector(shelvesSelector);

  useEffect(() => {
    dispatch(fetchBooklistAsync())
  }, [dispatch])


  return (
    <>
      <h1>WIP - Implementing Auth</h1>
      {status === Status.LOADING && <h1>Loading...</h1>}
      {status !== Status.LOADING && <BooksList
        readBooks={shelves.read}
        wantToRead={shelves.wantToRead}
        currentlyReading={shelves.currentlyReading} />}
    </>
  );

}

export default MyBooklist;
