import Book from "../../components/books/Book";
import { Status } from "../../constants/Status";

interface CuratedPicksState {
    nonFiction: Book[];
    fiction: Book[];
    status: Status;
    error: string | null;
}

const initialState: CuratedPicksState = {
    nonFiction: [],
    fiction: [],
    status: Status.IDLE,
    error: null
}