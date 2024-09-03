import Book from "../components/books/Book";
import { Shelf } from '../components/books/Book';

function splitBooksByShelf(books: Book[]) {

    const sortedBooks = {
        read: Array<Book>(),
        currentlyReading: Array<Book>(),
        wantToRead: Array<Book>()
    }

    books.forEach(book => {
        switch (book.shelf) {
            case Shelf.READ.valueOf():
                sortedBooks.read.push(book);
                break;
            case Shelf.CURRENTLY_READING.valueOf():
                sortedBooks.currentlyReading.push(book);
                break;
            case Shelf.WANT_TO_READ.valueOf():
                sortedBooks.wantToRead.push(book);
                break;
            }
    })

    return sortedBooks;
}

export default splitBooksByShelf;