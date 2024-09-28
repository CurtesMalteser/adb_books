import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import {
    fetchBestsellersAsync,
    fictionSelector,
    nonFictionSelector,
    statusSelector,
} from './NYTimesSlice';
import Book from '../../components/books/Book';
import BookShelf from '../../components/books/BookShelf';
import { Status } from '../../constants/Status';
import { Container } from 'react-bootstrap';
import Loader from '../loader/Loader';

const showBooks = (fiction: Book[], nonFiction: Book[]) => {
    return (
        <>
            <BookShelf key='fiction' title='Fiction' books={fiction.slice(0, 3)} />
            <BookShelf key='nonfiction' title='Non Fiction' books={nonFiction.slice(0, 3)} />
        </>
    )
};

const NYTimesBestsellers = () => {

    const dispatch = useAppDispatch();
    const status = useAppSelector(statusSelector);
    const fiction = useAppSelector(fictionSelector);
    const nonFiction = useAppSelector(nonFictionSelector);

    useEffect(() => {
        dispatch(fetchBestsellersAsync());
    }, [dispatch]);

    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            <h2>NY Times Bestsellers</h2>
            {status === Status.LOADING && <Loader />}
            {status === Status.IDLE && showBooks(fiction, nonFiction)}
        </Container>
    );
};

export default NYTimesBestsellers;