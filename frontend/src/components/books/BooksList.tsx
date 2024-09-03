import { useContext, useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';
import BookShelf from './BookShelf';
import splitBooksByShelf from '../../utils/BooksSorter';
import Book from './Book';
import { BookShelfContext } from '../../store/BookShelfContext';

function BooksList() {

    const { books } = useContext(BookShelfContext)

    const [readBooks, setReadBooks] = useState<Book[]>([])
    const [wantToRead, setWantToRead] = useState<Book[]>([])

    const [currentlyReading, setCurrentlyReading] = useState<Book[]>([])

    useEffect(() => {
        function addBooksToShelf() {
            const { read, currentlyReading, wantToRead } = splitBooksByShelf(books)
            setReadBooks(read)
            setCurrentlyReading(currentlyReading)
            setWantToRead(wantToRead)
        }
        addBooksToShelf()
    }, [books])



    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            < BookShelf title="Currently Reading" books={currentlyReading} />
            < BookShelf title="Want to read" books={wantToRead} />
            < BookShelf title="Read" books={readBooks} />
        </Container>
    );
}

export default BooksList;
