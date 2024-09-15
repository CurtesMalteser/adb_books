import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Book from './Book';
import BookCard from './BookCard';

interface BookShelfProps{
    title: string,
    books: Array<Book>,
}

const BookShelf: React.FC<BookShelfProps> = ({ title, books }) => {
    return (
        <div>
            <h3 style={{ paddingBottom: '20px' }}>{title}</h3>
            <Row xs={1} md={2} lg={3} className="g-4" style={{ paddingBottom: '20px' }}>
                {books.map((book) => <Col key={book.isbn13}><BookCard key={book.isbn13} book={book} /></Col>)}
            </Row>
            <hr />
        </div>
    )
}

export default BookShelf;
