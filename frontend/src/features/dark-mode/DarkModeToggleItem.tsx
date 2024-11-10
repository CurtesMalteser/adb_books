import { FunctionComponent, SVGProps } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import './DarkModeToggle.css';

export interface DarkModeToggleItemProps {
    Icon: FunctionComponent<SVGProps<SVGSVGElement>>;
    mode: string;
    selectedMode: string;
}

export default function DarkModeToggleItem({ Icon, mode, selectedMode }: DarkModeToggleItemProps) {
    const isSelected = mode === selectedMode;
    const className = isSelected ? 'icon-size dark-mode-toggle-selected' : 'icon-size  dark-mode-toggle'
    return (<Dropdown.Item active={isSelected} eventKey={mode}>
        <Icon className={className} /> {mode}
    </Dropdown.Item>
    )
}
