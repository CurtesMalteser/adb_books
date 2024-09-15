import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";
import { Status } from "../../constants/Status";
import { fetchFiction, fetchNonFiction } from "../../utils/BooksAPI";
import { RootState } from "../../app/store";
import { forkJoin, firstValueFrom } from "rxjs";

interface BestsellerState {
    nonFiction: Book[];
    fiction: Book[];
    status: Status;
    error: string | null;
}

const initialState: BestsellerState = {
    nonFiction: [],
    fiction: [],
    status: Status.IDLE,
    error: null
}

export const fetchBestsellersAsync = createAsyncThunk(
    'nytimes/fetchBestsellers',
    async () => {
        return await firstValueFrom(
            forkJoin({
                fiction: fetchFiction(),
                nonFiction: fetchNonFiction()
            })
        );
    }
);

export const nytimesSlice = createSlice({
    name: 'nytimes',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder.addCase(fetchBestsellersAsync.pending, (state) => {
            state.status = Status.LOADING;
            state.error = null;
        }).addCase(fetchBestsellersAsync.fulfilled, (state, action) => {
            state.status = Status.IDLE;
            state.error = null;
            state.fiction = action.payload.fiction;
            state.nonFiction = action.payload.nonFiction;
        }).addCase(fetchBestsellersAsync.rejected, (state, action) => {
            state.status = Status.FAILED;
            state.error = action.error.message || 'An error occurred';
        })
    }
});

export const statusSelector = (state: RootState) => state.nytimes.status;
export const fictionSelector = (state: RootState) => state.nytimes.fiction;
export const nonFictionSelector = (state: RootState) => state.nytimes.nonFiction;

export default nytimesSlice.reducer;
