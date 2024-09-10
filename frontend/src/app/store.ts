import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import booksReducer from '../features/home/booksSlice';
import nytimesReducer from '../features/bestseller/NYTimesSlice';
import myBooklistReducer from '../features/booklist/myBooklistSlice';

export const store = configureStore({
  reducer: {
    searchBooks: booksReducer,
    nytimes: nytimesReducer,
    myBooklist: myBooklistReducer
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
