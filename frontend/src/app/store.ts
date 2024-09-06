import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import booksReducer from '../features/home/booksSlice';

export const store = configureStore({
  reducer: {
    searchBooks: booksReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
