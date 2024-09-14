import Book from './Book';
import Dropdown from 'react-bootstrap/Dropdown';
import { Shelf } from './Book';
import { mapToLabel } from '../../utils/ShelfMapper';
import { DropdownButton } from 'react-bootstrap';

export interface DropdownBookItemsProps {
    book: Book,
    addToShelf: (isbn13: string, shelf: Shelf) => void,
    removeFromShelf: (isbn13: string) => void
}

const DropdownBookItems = ({ book, addToShelf }: {
    book: Book,
    addToShelf: (isbn13: string, shelf: Shelf) => void
}) => {
    return (
        <>
            {Object.values(Shelf).map((shelf) => (
                shelf !== book.shelf && <Dropdown.Item
                    key={shelf}
                    onClick={() => { addToShelf(book.isbn13, shelf) }} >
                    {mapToLabel(shelf)}
                </Dropdown.Item>
            ))}
        </>
    );
}

// TODO: Rename file to match this and not DropdownBookItems. Use git to remane
const BookShelfSelector: React.FC<DropdownBookItemsProps> = ({ book, addToShelf, removeFromShelf }) => {

    const shelfLabel = mapToLabel(book.shelf)

    return (
        <>
            <DropdownButton id="dropdown-basic-button" title={shelfLabel} className='mt-2'>
                <DropdownBookItems book={book} addToShelf={(isbn13, shelf) => addToShelf(isbn13, shelf)} />
                {
                    book.shelf && <Dropdown.Item
                        key='remove'
                        onClick={(key) => { removeFromShelf(book.isbn13) }} >Remove from Shelf</Dropdown.Item>
                }
            </DropdownButton>
        </>
    );
}

export default BookShelfSelector