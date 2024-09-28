import Book, { parseBook } from "../components/books/Book";
import { fetchAccessToken } from "../features/auth/authUtils";

const api = process.env.BOOKS_API_URL || 'http://127.0.0.1:5000'

const getHeaders = async () => fetchAccessToken()
  .then((token) => {
    return {
      Accept: 'application/json',
      Authorization: `Bearer ${token}`,
    }
  });

export const fetchReadBooklist = () =>
  getHeaders()
    .then((headers) => fetch(`${api}/booklist/read`, { headers }))
    .then((res) => res.json())
    .then((data) => data.books);

export const fetchWantToReadBooklist = () =>
  getHeaders()
    .then((headers) => fetch(`${api}/booklist/want-to-read`, { headers }))
    .then((res) => res.json())
    .then((data) => data.books);

export const fetchCurrentlyReadingBooklist = () =>
  getHeaders()
    .then((headers) => fetch(`${api}/booklist/currently-reading`, { headers }))
    .then((res) => res.json())
    .then((data) => data.books);

export const getBook = (id: string) =>
  getHeaders()
    .then((headers) => fetch(`${api}/book/${id}`, { headers }))
    .then((res) => res.json())
    .then((data) => data.book);

export const deleteBook = (id: string) =>
  getHeaders()
    .then((headers) => fetch(`${api}/book/${id}`, { headers, method: "DELETE" }))
    .then((res) => res.json());

export const postBook = (book: Book) =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/book`, {
        method: "POST",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          isbn13: book.isbn13,
          title: book.title,
          authors: book.authors,
          image: book.image,
          shelf: book.shelf!!.valueOf(),
        }),
      })).then((res) => res.json());

export const updateShelf = (id: string, shelf: string) =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/book/${id}`, {
        method: "PATCH",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ shelf }),
      }))
    .then((res) => res.json());

export const searchShelves = (query: string, maxResults: number) =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/search/shelves?q=${query}&limit=${maxResults}`, {
        method: "GET",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
      })).then((res) => res.json())
    .then((data) => data.books);

export const searchBooks = (query: string, maxResults: number) =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/search/books?q=${query}&limit=${maxResults}`, {
        method: "GET",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
      })).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)));

export const fetchNonFiction = () =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/ny-times/best-sellers/non-fiction`, {
        method: "GET",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
      })).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)))
    .catch((error) => {
      console.error('Error fetching fiction books', error);
      return [];
    });

export const fetchFiction = () =>
  getHeaders()
    .then((headers) =>
      fetch(`${api}/ny-times/best-sellers/fiction`, {
        method: "GET",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
      })
    ).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)))
    .catch((error) => {
      console.error('Error fetching fiction books', error);
      return [];
    });