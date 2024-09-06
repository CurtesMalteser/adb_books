import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import booksReducer from '../features/home/booksSlice';
import nytimesReducer from '../features/bestseller/NYTimesSlice';

export const store = configureStore({
  reducer: {
    searchBooks: booksReducer,
    nytimes: nytimesReducer,
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
