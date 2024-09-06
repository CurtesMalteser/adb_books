import Book from "../components/books/Book";
import { Shelf } from '../components/books/Book';

function splitBooksByShelf(books: Book[]) {

    const sortedBooks = {
        read: Array<Book>(),
        currentlyReading: Array<Book>(),
        wantToRead: Array<Book>()
    }
    // TODO: implement receive the shelf already in the book object from the backend
    // and remove the switch statement
    // TODO: implement slice and this function will removed
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