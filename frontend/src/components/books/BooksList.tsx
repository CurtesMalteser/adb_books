import { useContext, useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';
import BookShelf from './BookShelf';
import splitBooksByShelf from '../../utils/BooksSorter';
import Book from './Book';

interface BooksListProps {
    readBooks: Book[]
    wantToRead: Book[]
    currentlyReading: Book[]
}

const BooksList: React.FC<BooksListProps> = ({ readBooks, wantToRead, currentlyReading }) => {
    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            {readBooks.length > 0 && < BookShelf key='reading' title="Currently Reading" books={currentlyReading} />}
            {wantToRead.length > 0 && < BookShelf key='to_read' title="Want to read" books={wantToRead} />}
            {readBooks.length > 0 && < BookShelf key='read' title="Read" books={readBooks} />}
        </Container>
    );
}

export default BooksList;
