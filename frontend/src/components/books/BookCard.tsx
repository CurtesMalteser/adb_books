import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import Book from './Book';

function BookCard({ book }: { book: Book }) {

    const bookCover = book.image ?? '/book-placeholder.svg'
    const authors = book.authors ? book.authors.join(', ') : 'N/A'

    return (
        <Card border="primary" style={{ padding: '20px' }}>
            <Link to={`/book/${book.isbn13}`}>
                <Card.Img variant="top" src={bookCover} style={{ objectFit: 'contain', height: 380 }} />
            </Link>
            <Card.Body>
                <Link to={`/book/${book.isbn13}`}><Card.Title className='oneLine'>{book.title}</Card.Title></Link>
                <Card.Text className='oneLine'>{authors}</Card.Text>
            </Card.Body>
        </Card>
    )
}

export default BookCard;