import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import DropdownButton from 'react-bootstrap/DropdownButton';
import { mapToLabel } from '../../utils/ShelfMapper';
import DropdownBookItems from './DropdownBookItems';
import Book from './Book';

function BookCard( {book}: {book: Book}) {

    const addToShelf = (book: Book) => {
        console.group('📚 Book added to shelf')
        console.log('Implement the logic to add the book to the shelf')
        console.log(book)
        console.groupEnd()
      }

    const bookCover = book.image ?? '/book-placeholder.svg'
    const authors = book.authors ? book.authors.join(', ') : 'N/A'

    const shelfLabel = mapToLabel(book.shelf)

    return (
        <Card border="primary" style={{ padding: '20px' }}>
            <Card.Img variant="top" src={bookCover} style={{ objectFit: 'contain', height: 380 }} />
            <Card.Body>
                <Card.Title className='oneLine'>{book.title}</Card.Title>
                <Card.Text className='oneLine'>{authors}</Card.Text>
                <div className="d-flex">
                    <Link to={`/book/${book.isbn13}`}><Button variant="primary">Details</Button></Link>
                    <DropdownButton id="dropdown-basic-button" title={shelfLabel} style={{ paddingInlineStart: '10px' }}>
                        <DropdownBookItems book={book} addToShelf={() => addToShelf(book)} />
                    </DropdownButton>
                </div>
            </Card.Body>
        </Card>
    )
}

export default BookCard;