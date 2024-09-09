import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";
import { fetchBooklist, searchShelves } from "../../utils/BooksAPI";
import { RootState } from "../../app/store";
import { Status } from "../../constants/Status";

interface Shelves {
    read: Book[];
    wantToRead: Book[];
    currentlyReading: Book[];
}

interface BooksState {
    shelves: Shelves;
    status: Status;
    error: string | null;
}

const initialState: BooksState = {
    shelves: {
        read: [],
        wantToRead: [],
        currentlyReading: []
    },
    status: Status.IDLE,
    error: null
}

export const fetchBooklistAsync = createAsyncThunk(
    'books/searchBooks',
    async (payload: { searchTerm: string, maxResults: number }) => {
        const response = await fetchBooklist();
        return response;
    }
)

export const searchShelvesAsync = createAsyncThunk(
    'books/searchShelves',
    async (payload: { searchTerm: string, maxResults: number }) => {
        const response = await searchShelves(payload.searchTerm, payload.maxResults);
        return response;
    }
)

export const booklistSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder.addCase(fetchBooklistAsync.pending, (state) => {
            state.status = Status.LOADING;
            state.error = null;
        }).addCase(fetchBooklistAsync.fulfilled, (state, action) => {
            state.status = Status.IDLE;
            state.error = null;
            state.shelves = action.payload;
        })
            .addCase(fetchBooklistAsync.rejected, (state, action) => {
                state.status = Status.FAILED;
                state.error = action.error.message || 'An error occurred';
            })
    }
})

export const statusSelector = (state: RootState) => state.searchBooks.status;
export const booksSelector = (state: RootState) => state.searchBooks.books;

export default booklistSlice.reducer;