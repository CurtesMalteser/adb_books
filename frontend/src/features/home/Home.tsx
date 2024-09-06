import { Subject } from "rxjs";
import BookSearch from "../shelves/BookSearch";
import { booksSelector, searchBooksAsync } from "./booksSlice";

function HomePage() {

  const searchSubject = new Subject<string>();

  return (
    <>
      <h1>Loading...</h1>
      <BookSearch
        searchSubject={searchSubject}
        searchThunk={searchBooksAsync}
        booksSelector={booksSelector}
      />
    </>
  );

}

export default HomePage;
