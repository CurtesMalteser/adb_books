import { useEffect, useState, useContext } from 'react';
import BooksList from '../../components/books/BooksList';
import { getAll } from '../../utils/BooksAPI';


function MyBooklist() {
  // todo: set BookSearch to use the searchShelvesAsync thunk (from the shelvesSlice to be implemented) to search for books
  // const [isLoading, setIsLoading] = useState<boolean>(true)
  // const { books, setBooks } = useContext(BookShelfContext)

  // useEffect(() => {
  //   async function fetchBooks() {
  //     const data = await getAll()
  //     setBooks(data.books)
  //     setIsLoading(false)
  //   }

  //   if (books.length > 0) {
  //     setIsLoading(false)
  //   } else {

  //     fetchBooks()
  //   }
  // }, [books, setBooks])


  return (
    <>
      <h1>WIP - Implementing Auth</h1>
      {/* {isLoading && <h1>Loading...</h1>}
      {!isLoading && <BooksList />} */}
    </>
  );

}

export default MyBooklist;
