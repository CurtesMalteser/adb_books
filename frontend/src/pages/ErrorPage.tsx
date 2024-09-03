import Header from "../components/header/Header";

function ErrorPage() {
    return (
        <>
            <Header />
            <div style={{
                margin: '2rem auto',
                textAlign: 'center',
            }}>
                <h1>An Error occurre!</h1>
                <p>🚨 Could not find this page! 🚨</p>
            </div>
        </>
    )
}

export default ErrorPage;