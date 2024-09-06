import { useState } from 'react';
import BookShelf from '../../components/books/BookShelf';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { booksSelector, searchBooksAsync } from '../home/booksSlice';
import { useAppDispatch, useAppSelector } from '../../app/hooks';


function BookSearch() {

    const dispatch = useAppDispatch();
    const books = useAppSelector(booksSelector);

    const [searchTerm, setSearchTerm] = useState('')

    const searchHandler = async (searchTerm: string) => {
        setSearchTerm(searchTerm)
        dispatch(searchBooksAsync({ searchTerm, maxResults: 20 }))
        .then((response: any) => {
            console.log(response);
        })
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
            {(books?.length > 0) && <div style={{ marginTop: 20 }}>
                {
                    /*
                    TODO make a BookUI or something similar and map only what the UI expects her
                    -> BookShelfContext replace with slices as arg to query search/books and search/shelves
                    */
                }
                <BookShelf title={`Search Results: ${books.length}`} books={books} />
            </div>}
        </Container>
    );
};

export default BookSearch;