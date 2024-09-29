
import AppNavbar from './AppNavBar';
import MobileNavBar from './MobileNavBar';
import { useMediaQuery } from 'react-responsive';


function Header() {

  const isSmallScreen = useMediaQuery({maxWidth:996});

  return (
    <header>
      {isSmallScreen ? <MobileNavBar /> : <AppNavbar />}
    </header>
  );
}

export default Header;