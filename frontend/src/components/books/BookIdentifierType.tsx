import { IdentifierType, IndustryIdentifier } from './Book';


function BookIdentifierType({isbn}: { isbn: IndustryIdentifier }) {
    const type = IdentifierType[`${isbn.type}` as keyof typeof IdentifierType]
    return (<><b>{type}:</b> {isbn.identifier}<br /></>)
}

export default BookIdentifierType;