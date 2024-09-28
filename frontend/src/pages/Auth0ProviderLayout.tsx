import { Outlet } from 'react-router-dom';
import Header from '../components/header/Header';
import { Auth0ProviderWithNavigate } from '../features/auth/Auth0ProviderWithNavigate';


function Auth0ProviderLayout() {
    return (
        <Auth0ProviderWithNavigate>
            <Header />
            <main className='App'>
                <Outlet />
            </main>
        </Auth0ProviderWithNavigate>
    )
}

export default Auth0ProviderLayout;