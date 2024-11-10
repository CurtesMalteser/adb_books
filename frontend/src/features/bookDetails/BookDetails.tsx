import { useParams } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import { IdentifierType, Shelf } from "../../components/books/Book";
import BookIdentifierType from "../../components/books/BookIdentifierType";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import BookRating from "../../components/books/BookRating";
import BookShelfSelector from "../../components/books/DropdownBookItems";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { bookSelector, fetchBookDetailsAsync, removeFromShelfAsync, statusSelector, updateShelfAsync } from "./bookDetailsSlice";
import { useEffect } from "react";
import { Status } from "../../constants/Status";
import Loader from "../loader/Loader";
import BookDetailsError from "./BookDetailsError";

// TODO: add slice and thunk to update book on BE
function BookDetails() {

    const { id } = useParams<{ id: string }>();

    const dispatch = useAppDispatch();

    const status = useAppSelector(statusSelector);
    const book = useAppSelector(bookSelector);

    const authorLabel = (book?.authors?.length ?? 1) > 1 ? "Authors" : "Author";
    const authors = book?.authors ? book.authors.join(', ') : 'N/A';
    const categoryLabel = (book?.subjects?.length ?? 1) > 1 ? "Categories" : "Category";


    const addToShelf = (isbn13: string, shelf: Shelf) => {
        dispatch(updateShelfAsync({ isbn13, shelf }))
    }

    const removeFromShelf = (isbn13: string) => {
        dispatch(removeFromShelfAsync(isbn13))
    }

    useEffect(() => {
        id && dispatch(fetchBookDetailsAsync(id))
    }, [id, dispatch])

    return (
        <Container className="md-6" style={{ marginTop: 20, marginBottom: 20, marginLeft: "auto", marginRight: "auto" }} >
            {status === Status.LOADING && <Loader />}
            {status === Status.FAILED && <BookDetailsError />}
            {status === Status.IDLE &&
                <Row md={8}>
                    {
                        book && <>
                            <Col sm={12} md={6} lg={4}>
                                <img style={{ height: 380 }} src={book.image} alt={book.title} />
                            </Col>
                            <Col>
                                <h2>{book.title}</h2>
                                <h3>{book.subtitle}</h3>
                                <p><b>{authorLabel}:</b> {authors}</p>
                                <BookRating rating={book.rating} ratingsCount={book.rating} />
                                <BookShelfSelector book={book} addToShelf={addToShelf} removeFromShelf={removeFromShelf}/>
                                <hr />
                                <p>{book.synopsis}</p>
                                <hr />
                                <p>
                                    {book.subjects && <><b>{categoryLabel}:</b> {book.subjects.join(", ")}<br /></>}
                                    {book.publisher && <><b>Publisher:</b> {book.publisher} <br /></>}
                                    <b>Published Date:</b> {book.datePublished} <br />
                                    <b>Page Count:</b> {book.pages} <br />
                                    <BookIdentifierType key={IdentifierType.ISBN_10} isbn={{
                                        type: IdentifierType.ISBN_10,
                                        identifier: book.isbn,
                                    }} />
                                    <BookIdentifierType key={IdentifierType.ISBN_13} isbn={{
                                        type: IdentifierType.ISBN_13,
                                        identifier: book.isbn13,
                                    }} />
                                </p>
                            </Col>
                        </>
                    }
                </Row>
            }
        </Container>
    );
};

export default BookDetails;
