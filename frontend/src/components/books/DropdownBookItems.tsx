import Book from './Book';
import Dropdown from 'react-bootstrap/Dropdown';
import { Shelf } from './Book';
import { mapToLabel } from '../../utils/ShelfMapper';

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
    )
}

export default DropdownBookItems