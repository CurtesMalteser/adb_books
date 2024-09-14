import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";
import { Status } from "../../constants/Status";
import { getBook } from "../../utils/BooksAPI";
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
    }
})

export const statusSelector = (state: RootState) => state.bookDetails.status;
export const bookSelector = (state: RootState) => state.bookDetails.book;

export default bookDetailsSlice.reducer;