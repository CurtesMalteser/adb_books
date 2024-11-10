import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import booksReducer from '../features/home/booksSlice';
import nytimesReducer from '../features/bestseller/NYTimesSlice';
import myBooklistReducer from '../features/booklist/myBooklistSlice';
import bookDetailsReducer from '../features/bookDetails/bookDetailsSlice';
import darkModeReducer from '../features/dark-mode/darkModeSlice';

export const store = configureStore({
  reducer: {
    searchBooks: booksReducer,
    nytimes: nytimesReducer,
    myBooklist: myBooklistReducer,
    bookDetails: bookDetailsReducer,
    darkMode: darkModeReducer,
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
