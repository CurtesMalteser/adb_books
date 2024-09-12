import { parseBook } from "../components/books/Book";

const api = process.env.BOOKS_API_URL || 'http://127.0.0.1:5000'

let token = localStorage.token;

const header = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9';
const payload = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1haWwiOiJqb2huLmRvZUBkb2UuY29tIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJib29rOnNhdmUiLCJib29rOmdldCIsImJvb2s6ZGVsZXRlIl19';
const signature = 'sBr7N20iIwugvL0ix2m05oV1Op3Q1oAdhW05KhUbZWA';

if (!token) token = localStorage.token = `${header}.${payload}.${signature}`;

const headers = {
  Accept: "application/json",
  Authorization: `Bearer ${token}`,
};

export const fetchReadBooklist = () =>
  fetch(`${api}/booklist/read`, { headers })
    .then((res) => res.json())
    .then((data) => data);

export const fetchWantToReadBooklist = () =>
  fetch(`${api}/booklist/want-to-read`, { headers })
    .then((res) => res.json())
    .then((data) => data);

export const fetchCurrentlyReadingBooklist = () =>
  fetch(`${api}/booklist/currently-reading`, { headers })
    .then((res) => res.json())
    .then((data) => data);

export const getBook = (id: string) =>
  fetch(`${api}/book/${id}`, { headers })
    .then((res) => res.json())
    .then((data) => data.book);

export const update = (id: string, shelf: string) =>
  fetch(`${api}/books/${id}`, {
    method: "PATCH",
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