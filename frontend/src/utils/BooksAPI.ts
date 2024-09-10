import { parseBook } from "../components/books/Book";

const api = process.env.BOOKS_API_URL || 'http://127.0.0.1:5000'

let token = localStorage.token;

const head = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9';
const payload = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1haWwiOiJqb2huLmRvZUBkb2UuY29tIiwiaWF0IjoxNTE2MjM5MDIyLCJyb2xlIjoiYm9vazpzYXZlIn0';
const signature = 'FB36NBKLutcaVMDnBl4y0Dwturq38L3GDAqtdgQt0dc';

if (!token) token = localStorage.token = `${head}.${payload}.${signature}`;

const headers = {
  Accept: "application/json",
  Authorization: `Bearer ${token}`,
};

export const fetchBooklist = () =>
  fetch(`${api}/booklist`, { headers })
    .then((res) => res.json())
    .then((data) => data);

export const getBook = (id: string) =>
  fetch(`${api}/books/${id}`, { headers })
    .then((res) => res.json())
    .then((data) => data.book);

export const update = (id: string, shelf: string) =>
  fetch(`${api}/books/${id}`, {
    method: "PUT",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ shelf }),
  }).then((res) => res.json());

export const searchShelves = (query: string, maxResults: number) =>
  fetch(`${api}/search/shelves?q=${query}&limit=${maxResults}`, {
    method: "GET",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  }).then((res) => res.json())
    .then((data) => data.books);

export const searchBooks = (query: string, maxResults: number) =>
  fetch(`${api}/search/books?q=${query}&limit=${maxResults}`, {
    method: "GET",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  }).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)));

export const fetchNonFiction = () =>
  fetch(`${api}/ny-times/best-sellers/non-fiction`, {
    method: "GET",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  }).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)));

export const fetchFiction = () =>
  fetch(`${api}/ny-times/best-sellers/fiction`, {
    method: "GET",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  }).then((res) => res.json())
    .then((data) => data.books.map((book: any) => parseBook(book)));