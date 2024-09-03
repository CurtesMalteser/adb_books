import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import Book from './Book';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import { Shelf } from './Book';
import { mapToLabel } from '../../utils/ShelfMapper';

function DropdownBookItems({ book, addToShelf }: { book: Book, addToShelf: (book: Book) => void }) {
    return (
        <>
            {Object.values(Shelf).map((shelf) => (
                shelf !== book.shelf && <Dropdown.Item key={shelf} onClick={() => {
                    book.shelf = shelf
                    addToShelf(book)
                }} > {mapToLabel(shelf)} </Dropdown.Item>
            )
            )}
        </>
    )
}

function BookCard(book: Book, addToShelf: (book: Book) => void) {

    const bookCover = book.imageLinks ? book.imageLinks.thumbnail : '/book-placeholder.svg'
    const authors = book.authors ? book.authors.join(', ') : 'N/A'

    const shelfLabel = mapToLabel(book.shelf)

    return (
        <Card border="primary" style={{ padding: '20px' }}>
            <Card.Img variant="top" src={bookCover} style={{ objectFit: 'contain', height: 380 }} />
            <Card.Body>
                <Card.Title className='oneLine'>{book.title}</Card.Title>
                <Card.Text className='oneLine'>{authors}</Card.Text>
                <div className="d-flex">
                    <Link to={`/book/${book.id}`}><Button variant="primary">Details</Button></Link>
                    <DropdownButton id="dropdown-basic-button" title={shelfLabel} style={{ paddingInlineStart: '10px' }}>
                        <DropdownBookItems book={book} addToShelf={() => addToShelf(book)} />
                    </DropdownButton>
                </div>
            </Card.Body>
        </Card>
    )
}

export default BookCard;