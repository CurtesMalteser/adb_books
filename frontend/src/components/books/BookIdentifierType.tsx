import { IndustryIdentifier } from './Book';

const BookIdentifierType = ({isbn}: { isbn: IndustryIdentifier }) =>  (<><b>{isbn.type}:</b> {isbn.identifier}<br /></>)

export default BookIdentifierType;