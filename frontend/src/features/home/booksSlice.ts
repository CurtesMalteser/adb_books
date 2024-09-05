import { createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";

interface BooksState {
    books: Book[];
    loading: boolean;
    error: string | null;
}

const initialState: BooksState = {
    books: [],
    loading: false,
    error: null
}

export const booksSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {
    },
    extraReducers: (builder) => {}
})

export default booksSlice.reducer;