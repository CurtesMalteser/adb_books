import { ReactComponent as Sun } from '../../assets/svg/sun.svg';
import { ReactComponent as Moon } from '../../assets/svg/moon.svg';
import { ReactComponent as Auto } from '../../assets/svg/dark-light.svg';
import DropdownButton from 'react-bootstrap/DropdownButton';
import DarkModeToggleItem from './DarkModeToggleItem';
import './DarkModeToggle.css';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { darkModeSelector, setDarkMode } from './darkModeSlice';

function TitleSelection(selectedMode: string) {
    switch (selectedMode) {
        case 'light':
            return <Sun className='icon-size' /> 
        case 'dark':
            return <Moon className='icon-size' /> 
        default:
            return <Auto className='icon-size' /> 
    }
}

function DarkModeToggle({className}: {className?: string}) {
    const dispatch = useAppDispatch();
    const isDarkMode = useAppSelector(darkModeSelector)

    const setPreferredTheme = (selectedMode: string) => {
        dispatch(setDarkMode(selectedMode))
    };

    return (
        <DropdownButton
            key={isDarkMode}
            id={`dropdown-split-variants-${isDarkMode}`}
            className={`dark-mode-dropdown ${className}`}
            title={ TitleSelection(isDarkMode) }
            onSelect={(e) => setPreferredTheme(e ?? 'auto')}
        >
            <DarkModeToggleItem Icon={Sun} mode='light' selectedMode={isDarkMode} />
            <DarkModeToggleItem Icon={Moon} mode='dark' selectedMode={isDarkMode} />
            <DarkModeToggleItem Icon={Auto} mode='auto' selectedMode={isDarkMode} />
        </DropdownButton>
    );
};

export default DarkModeToggle;