import { Subject } from "rxjs";
import BookSearch from "../shelves/BookSearch";
import {
  booksSelector,
  searchBooksAsync,
  statusSelector,
  errorSelector,
} from "./booksSlice";
import NYTimesBestsellers from "../bestseller/NYTimesBestsellers";

function HomePage() {

  const searchSubject = new Subject<string>();

  return (
    <>
      <BookSearch
        searchSubject={searchSubject}
        searchThunk={searchBooksAsync}
        booksSelector={booksSelector}
        statusSelector={statusSelector}
        errorSelector={errorSelector}
      />
      <NYTimesBestsellers />
    </>
  );

}

export default HomePage;
