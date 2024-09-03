import { Shelf } from '../components/books/Book';

export function mapToLabel(value?: string): string {
    switch (value) {
        case Shelf.READ.valueOf():
            return "Read";
        case Shelf.WANT_TO_READ.valueOf():
            return "Want to Read";
        case Shelf.CURRENTLY_READING.valueOf():
            return "Currently Reading";
        default:
            return "Add to shelf";
    }
}