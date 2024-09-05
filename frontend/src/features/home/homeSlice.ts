import { createSlice } from "@reduxjs/toolkit";
import Book from "../../components/books/Book";

interface Hometate {
    books: Book[];
    loading: boolean;
    error: string | null;
}

const initialState: Hometate = {
    books: [],
    loading: false,
    error: null
}

export const homeSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {
    },
    extraReducers: (builder) => {}
})

export default homeSlice.reducer;