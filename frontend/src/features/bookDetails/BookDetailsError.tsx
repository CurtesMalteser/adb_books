import './BookDetailsError.css';
import ROUTES from "../../constants/Routes";
import Loader from "../loader/Loader";

const BookDetailsError = () => {
    return (
        <>
            <div className='error-container'>
            <h2>We couldn't find the book you're looking for...</h2>
            <a href={ROUTES.HOME}>Go back to the home page</a>
            </div>
            <Loader />
        </>
    );
};

export default BookDetailsError;