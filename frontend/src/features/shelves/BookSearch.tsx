import { useState, useContext } from 'react';
import { searchBooks } from '../../utils/BooksAPI';
import BookShelf from '../../components/books/BookShelf';
import Book from '../../components/books/Book';
import Container from 'react-bootstrap/Container';
import { BookShelfContext } from '../../store/BookShelfContext';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


function BookSearch() {

    const { books } = useContext(BookShelfContext)

    const [searchTerm, setSearchTerm] = useState('')
    const [searchResults, setSearchResults] = useState<Book[]>([])

    const searchHandler = async (searchTerm: string) => {
        setSearchTerm(searchTerm)
        try {
            const response = await searchBooks(searchTerm, 20);

            if (response?.error || response?.items === 0) {
                setSearchResults([])
            } else {
                const sortedBooks = response.map((book: Book) => book)

                setSearchResults(sortedBooks)
            }
        } catch (error) {
            setSearchResults([])
        }
    }

    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            <Row>
                <Col>
                    <Form.Control
                        className="mr-sm-2"
                        type="text"
                        placeholder='Search for books...'
                        value={searchTerm}
                        onChange={(e) => searchHandler(e.target.value)}
                    />
                </Col>
                <Col>
                    <Button variant="primary" onClick={() => searchHandler(searchTerm)}>Search</Button>
                </Col>
            </Row>
            {(searchResults?.length > 0) && <div style={{ marginTop: 20 }}>
                {
                    /*
                    TODO make a BookUI or something similar and map only what the UI expects her
                    -> BookShelfContext replace with slices as arg to query search/books and search/shelves
                    */
                }
                <BookShelf title={`Search Results: ${searchResults.length}`} books={searchResults} />
            </div>}
        </Container>
    );
};

export default BookSearch;