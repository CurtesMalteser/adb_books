import {
  catchError,
  firstValueFrom,
  from,
  map,
  of,
  switchMap,
} from "rxjs";
import Book, { parseBook } from "../components/books/Book";
import { fetchAccessToken } from "../features/auth/authUtils";

const api = process.env.BOOKS_API_URL || 'http://127.0.0.1:5000'

const getHeaders = () => from(fetchAccessToken()).pipe(
  map((token) => ({
    Accept: 'application/json',
    Authorization: `Bearer ${token}`,
  }))
)

const performFetch = (url: string, options: RequestInit = {}) => firstValueFrom(
  getHeaders().pipe(
    switchMap((headers) => {
      const mergedHeaders = { ...headers, ...options.headers };
      return from(fetch(url, { ...options, headers: mergedHeaders })).pipe(
        switchMap((res) => from(res.json())),
        catchError((error) => {
          console.error(`❌ Error fetching ${url}. ${error}`);
          return of({})
        })
      )
    })
  ));

export const fetchReadBooklist = () => performFetch(`${api}/booklist/read`)
  .then((data) => data.books);

export const fetchWantToReadBooklist = () => performFetch(`${api}/booklist/want-to-read`)
  .then((data) => data.books);

export const fetchCurrentlyReadingBooklist = () => performFetch(`${api}/booklist/currently-reading`)
  .then((data) => data.books);

export const getBook = (id: string) => performFetch(`${api}/book/${id}`)
  .then((data) => data.book);

export const deleteBook = (id: string) => performFetch(`${api}/book/${id}`, { method: "DELETE" })

export const postBook = (book: Book) => performFetch(`${api}/book`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    isbn13: book.isbn13,
    title: book.title,
    authors: book.authors,
    image: book.image,
    shelf: book.shelf!!.valueOf(),
  }),
});

export const updateShelf = (id: string, shelf: string) => performFetch(`${api}/book/${id}`, {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ shelf }),
});

export const searchShelves = (query: string, maxResults: number) => performFetch(`${api}/search/shelves?q=${query}&limit=${maxResults}`)
  .then((data) => data.books);

export const searchBooks = (query: string, maxResults: number) => performFetch(`${api}/search/books?q=${query}&limit=${maxResults}`)
  .then((data) => data.books.map((book: any) => parseBook(book)));

export const fetchNonFiction = () => performFetch(`${api}/ny-times/best-sellers/non-fiction`)
  .then((data) => data.books.map((book: any) => parseBook(book)))

export const fetchFiction = () => performFetch(`${api}/ny-times/best-sellers/fiction`)
  .then((data) => data.books.map((book: any) => parseBook(book)))
