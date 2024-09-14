import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book, { Shelf } from "../../components/books/Book";
import { Status } from "../../constants/Status";
import { getBook, postBook, updateShelf } from "../../utils/BooksAPI";
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
    async ({ isbn13, shelf }: { isbn13: string, shelf: Shelf }, { getState }) => {
        const state = getState() as RootState;
        const book = state.bookDetails.book;

        if (!book) {
            throw new Error(`Book with ISBN ${isbn13} not found in state`);
        }

        if (book.shelf === null) {
             await postBook({ ...book, shelf });
        } else {
             await updateShelf(isbn13, shelf);
        }

        return { ...book, shelf };
    }
);

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
            console.log(`📚 Book added to shelf: ${action.payload?.shelf}`)
            state.book = action.payload;
        })
        .addCase(updateShelfAsync.rejected, (state, action) => {
            console.error(action.error)
            state.status = Status.FAILED;
            state.error = action.error.message || 'An error occurred';
        })
    }
})

export const statusSelector = (state: RootState) => state.bookDetails.status;
export const bookSelector = (state: RootState) => state.bookDetails.book;

export default bookDetailsSlice.reducer;