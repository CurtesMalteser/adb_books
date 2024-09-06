import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import {
    fetchBestsellersAsync,
    fictionSelector,
    nonFictionSelector,
    statusSelector,
} from './NYTimesSlice';
import Book from '../../components/books/Book';

const showBooks = (fiction: Book[], nonFiction: Book[]) => {
    return (
        <>
            <h3>Fiction</h3>
            {fiction && fiction.length > 0 && (
                fiction.map((book: Book) => <div key={book.id}>{book.title}</div>)
            )}
            <h3>Non-Fiction</h3>
            {nonFiction && nonFiction.length > 0 && (
                nonFiction.map((book: Book) => <div key={book.id}>{book.title}</div>)
            )}
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