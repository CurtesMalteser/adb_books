import { useLoaderData } from "react-router-dom";
import { getBook } from "../../utils/BooksAPI";
import Container from 'react-bootstrap/Container';
import Book, { IdentifierType } from "../../components/books/Book";
import BookIdentifierType from "../../components/books/BookIdentifierType";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import BookRating from "../../components/books/BookRating";


function BookDetails() {

    const book = useLoaderData() as Book;
    const authorLabel = (book.authors?.length ?? 1) > 1 ? "Authors" : "Author";
    const authors = book.authors ? book.authors.join(', ') : 'N/A';
    const categoryLabel = (book.subjects?.length ?? 1) > 1 ? "Categories" : "Category";

    return (
        <Container className="md-6" style={{ marginTop: 20, marginBottom: 20, marginLeft: "auto", marginRight: "auto" }} >
            <Row md={8}>
                <Col sm={12} md={6} lg={4}>
                    <img style={{ height: 380 }} src={book.image} alt={book.title} />
                </Col>
                <Col>
                    <h2>{book.title}</h2>
                    <h3>{book.subtitle}</h3>
                    <p><b>{authorLabel}:</b> {authors}</p>
                    <BookRating rating={book.rating} ratingsCount={book.rating} />
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
                            }}/>
                        <BookIdentifierType key={IdentifierType.ISBN_13} isbn={{
                            type: IdentifierType.ISBN_13,
                            identifier: book.isbn13,
                            }}/>
                    </p>
                </Col>
            </Row>
        </Container>
    );
};

export default BookDetails;

export async function loader({ request, params }: { request: any, params: any }) {
    return await getBook(params.id)
}