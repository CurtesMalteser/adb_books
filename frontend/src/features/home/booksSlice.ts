import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";
import { searchBooks } from "../../utils/BooksAPI";
import { RootState } from "../../app/store";
import { Status } from "../../constants/Status";

interface BooksState {
    books: Book[];
    status: Status;
    error: string | null;
}

const initialState: BooksState = {
    books: [],
    status: Status.IDLE,
    error: null
}

export const searchBooksAsync = createAsyncThunk(
    'books/searchBooks',
    async (payload: {searchTerm: string, maxResults: number}) => {
        if(payload.searchTerm === '') return [];
        else return searchBooks(payload.searchTerm, payload.maxResults);
    }
)

export const booksSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder.addCase(searchBooksAsync.pending, (state) => {
            state.status = Status.LOADING;
            state.error = null;
        }).addCase(searchBooksAsync.fulfilled, (state, action) => {
            state.status = Status.IDLE;
            state.error = null;
            state.books = action.payload;
        })
        .addCase(searchBooksAsync.rejected, (state, action) => {
            state.status = Status.FAILED;
            state.books = [];
            state.error = action.error.message || 'An error occurred';
        })
    }
})

export const statusSelector = (state: RootState) => state.searchBooks.status;
export const booksSelector = (state: RootState) => state.searchBooks.books;
export const errorSelector = (state: RootState) => state.searchBooks.error;

export default booksSlice.reducer;