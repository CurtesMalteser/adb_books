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
    id: string;
    title: string;
    subtitle: string;
    authors: string[];
    datePublished?: string
    subjects?: string[];
    image?: string;
    shelf?: Shelf;
    publisher?: string;
    rating: number;
    synopsis: string;
    pages: number;
    msrp: number;
    isbn: string;
    isbn13: string;
    language: string;
}

export function parseBook(data: any): Book {
    return {
        ...data,
        datePublished: data.date_published
    };
}

export default Book;