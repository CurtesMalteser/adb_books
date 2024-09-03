import { Outlet } from 'react-router-dom';
import Header from '../components/header/Header';


function RouteLayout() {
    return (
        <>
            <Header />
            <main className='App'>
                <Outlet />
            </main>
        </>
    )
}

export default RouteLayout;