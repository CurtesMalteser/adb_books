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

const showBooks = (fiction: Book[], nonFiction: Book[]) => {
    return (
        <>
            <BookShelf title='Fiction' books={fiction.slice(0, 3)}/>
            <BookShelf title='Non Fiction' books={nonFiction.slice(0, 3)}/>
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
        <>
            <h2>NY Times Bestsellers</h2>
            {status === 'loading' && <h1>Loading...</h1>}
            {status === 'idle' && showBooks(fiction, nonFiction)}
        </>
    );
};

export default NYTimesBestsellers;