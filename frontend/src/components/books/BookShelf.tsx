
import { useContext } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Book from './Book';
import BookCard from './BookCard';
import { BookShelfContext } from '../../store/BookShelfContext';
import { update } from '../../utils/BooksAPI';


function BookShelf({ title, books }: { title: string, books: Array<Book> }) {

    const { addToShelf } = useContext(BookShelfContext)

    function addToaddBooksToShelf(book: Book) {
        async function addBooksToShelf() {
            try {
                await update(book.id, book.shelf!!)
                addToShelf(book)
            } catch (error) {
                console.error(error)
            }
        }
        addBooksToShelf()
    }

    return (
        <div>
            <h3 style={{ paddingBottom: '20px' }}>{title}</h3>
            <Row xs={1} md={2} lg={3} className="g-4" style={{ paddingBottom: '20px' }}>
                {books.map((book) => <Col key={book.id}>{BookCard(book, addToaddBooksToShelf)}</Col>)}
            </Row>
            <hr />
        </div>
    )
}

export default BookShelf;
