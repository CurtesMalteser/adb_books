import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book, { Shelf } from "../../components/books/Book";
import { Status } from "../../constants/Status";
import { getBook, updateShelf } from "../../utils/BooksAPI";
import { RootState } from "../../app/store";

interface BookDetailsState {
    book: Book | null;
    status: Status;
    error: string | null;
}

const initialState: BookDetailsState = {
    book: null,
    status: Status.IDLE,
    error: null
}

export const fetchBookDetailsAsync = createAsyncThunk(
    'bookDetails/fetchBook',
    async (id: string) => {
        const response = getBook(id)
        return response;
    }
)

export const updateShelfAsync = createAsyncThunk(
    'bookDetails/updateShelf',
    async ({isbn13, shelf}: {isbn13: string, shelf: Shelf}) => {
        // todo: add logic to post book to server if the previous shelf was null
        // else update the shelf
        const response = updateShelf(isbn13, shelf)
        await response;
        return shelf;
    }
)

export const bookDetailsSlice = createSlice({
    name: 'bookDetails',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder.addCase(fetchBookDetailsAsync.pending, (state) => {
            state.status = Status.LOADING;
            state.error = null;
        }).addCase(fetchBookDetailsAsync.fulfilled, (state, action) => {
            state.status = Status.IDLE;
            state.error = null;
            state.book = action.payload;
        })
        .addCase(fetchBookDetailsAsync.rejected, (state, action) => {
            state.status = Status.FAILED;
            state.error = action.error.message || 'An error occurred';
        })
        .addCase(updateShelfAsync.pending, (state) => {
            state.status = Status.LOADING;
            state.error = null;
        }).addCase(updateShelfAsync.fulfilled, (state, action) => {
            state.status = Status.IDLE;
            state.error = null;
            const book = state.book;
            if(book) {
                book.shelf = action.payload;
                state.book = book;
            }
        })
        .addCase(updateShelfAsync.rejected, (state, action) => {
            state.status = Status.FAILED;
            state.error = action.error.message || 'An error occurred';
        })
    }
})

export const statusSelector = (state: RootState) => state.bookDetails.status;
export const bookSelector = (state: RootState) => state.bookDetails.book;

export default bookDetailsSlice.reducer;