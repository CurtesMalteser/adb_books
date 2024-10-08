import { useEffect, useState } from 'react';
import BookShelf from '../../components/books/BookShelf';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { debounceTime, Subject } from 'rxjs';
import { RootState } from '../../app/store';
import Book from '../../components/books/Book';
import { Status } from '../../constants/Status';

interface BookSearchProps {
    searchSubject: Subject<string>;
    statusSelector: (state: RootState) => Status;
    errorSelector: (state: RootState) => string | null;
    searchThunk: (params: { searchTerm: string; maxResults: number }) => any;
    booksSelector: (state: RootState) => Book[];
}

const BookSearch: React.FC<BookSearchProps> = ({
    searchSubject,
    booksSelector,
    searchThunk,
    statusSelector,
    errorSelector,
 }) => {

    const dispatch = useAppDispatch();
    const status = useAppSelector(statusSelector);
    const books = useAppSelector(booksSelector);
    const error = useAppSelector(errorSelector);

    const [searchTerm, setSearchTerm] = useState('');

    const searchHandler = async (searchTerm: string) => dispatch(searchThunk({ searchTerm, maxResults: 10 }));

    useEffect(() => {
        const subscription = searchSubject
            .pipe(debounceTime(600))
            .subscribe(searchHandler);

        return () => {
            subscription.unsubscribe();
        };
    }, []);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
        searchSubject.next(e.target.value);
    };

    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            <Row>
                <Col>
                    <Form.Control
                        className="mr-sm-2"
                        type="text"
                        placeholder='Search for books...'
                        value={searchTerm}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col>
                    <Button variant="primary" onClick={() => searchHandler(searchTerm)}>Search</Button>
                </Col>
            </Row>
            {(books?.length > 0) && <div style={{ marginTop: 20 }}>
                <BookShelf title={`Search Results: ${books.length}`} books={books} />
            </div>}
            {
                // Show nice loading, possibly a book card with lottie book animation
                status === Status.LOADING && <h1>Loading...</h1>
            }
            {error && <h1>No books found</h1>}
        </Container>
    );
};

export default BookSearch;