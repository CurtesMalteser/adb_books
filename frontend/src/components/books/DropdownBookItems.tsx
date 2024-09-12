import Book from './Book';
import Dropdown from 'react-bootstrap/Dropdown';
import { Shelf } from './Book';
import { mapToLabel } from '../../utils/ShelfMapper';
import { DropdownButton } from 'react-bootstrap';

export interface DropdownBookItemsProps {
    book: Book,
    addToShelf: (book: Book) => void,
}

const DropdownBookItems: React.FC<DropdownBookItemsProps> = ({ book, addToShelf }) => {
    return (
        <>
            {Object.values(Shelf).map((shelf) => (
                shelf !== book.shelf && <Dropdown.Item key={shelf} onClick={() => {
                    // book.shelf = shelf
                    addToShelf(book)
                }} > {mapToLabel(shelf)} </Dropdown.Item>
            )
            )}
        </>
    );
}

// TODO: Rename file to match this and not DropdownBookItems. Use git to remane
const BookShelfSelector: React.FC<DropdownBookItemsProps> = ({ book, addToShelf }) => {

    const shelfLabel = mapToLabel(book.shelf)

    return (
        <>
            <DropdownButton id="dropdown-basic-button" title={shelfLabel} className='mt-2'>
                <DropdownBookItems book={book} addToShelf={() => addToShelf(book)} />
            </DropdownButton>
        </>
    );
}

export default BookShelfSelector