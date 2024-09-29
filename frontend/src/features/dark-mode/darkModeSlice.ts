import { createSelector, createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';

const getMode = (mode: string) => mode === 'auto' ? prefersDarkMode() : mode;

const setAppMode = (mode: string) => {
    localStorage.setItem('app-mode', mode); 
    const selectedMode = getMode(mode);
    document.querySelector('html')?.setAttribute('data-bs-theme', selectedMode);
    return mode;
};

const prefersDarkMode = () => window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

const loadAppMode = () => {
    const mode = localStorage.getItem('app-mode');
    console.log('loadAppMode', mode);
    return mode ? mode : prefersDarkMode();
};

interface DarkModeState {
    mode: string;
};

const initialState: DarkModeState = {

    mode: setAppMode(loadAppMode()),
};

const darkModeSlice = createSlice({
    name: 'darkMode',
    initialState,
    reducers: {
        setDarkMode: (state, action: PayloadAction<string>) => {
            state.mode = action.payload;
            setAppMode(state.mode);
        },
    },
});

export const { setDarkMode } = darkModeSlice.actions;

export const darkModeSelector = (state: RootState) => state.darkMode.mode;
export const isDarkModeSelector = createSelector(
    (state: RootState) => state.darkMode.mode,
    (mode) => getMode(mode) === 'dark'
);

export default darkModeSlice.reducer;