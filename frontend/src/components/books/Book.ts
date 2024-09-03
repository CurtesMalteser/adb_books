export enum IdentifierType {
    ISBN_10 = "ISBN-10",
    ISBN_13 = "ISBN-13"
}

export interface ImageLinks {
    smallThumbnail: string;
    thumbnail: string;
}

export interface IndustryIdentifier {
    type: IdentifierType;
    identifier: string;
}

export enum Shelf {
    READ = "read",
    WANT_TO_READ = "wantToRead",
    CURRENTLY_READING = "currentlyReading"
}

interface Book {
    id: number;
    title: string;
    subtitle: string;
    authors?: [string];
    publishedDate: number;
    categories?: [string];
    imageLinks: ImageLinks;
    industryIdentifiers: [IndustryIdentifier];
    shelf?: Shelf;
    publisher: string;
    description: string;
    pageCount: number;
    averageRating: number;
    ratingsCount: number;
    language: string;
}

export default Book;