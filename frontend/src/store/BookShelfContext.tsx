import { createContext, useState } from "react";
import Book from "../components/books/Book";


export const BookShelfContext = createContext({
  books: Array<Book>(),
  setBooks: (books: Array<Book>) => { },
  addToShelf: (book: Book) => { },
});

export default function BookShelfContextProvider({ children }: { children: React.ReactNode }) {

  const [books, setBooks] = useState<Book[]>([])

  function addToShelf(book: Book) {
    const index = books.findIndex(b => b.id === book.id)
    if(index === -1) {
      setBooks([...books, book])
    } else {
      const updatedBooks = [...books]
      updatedBooks[index] = book
      setBooks(updatedBooks)
    }
  }

 const ctx = { books, setBooks, addToShelf }

  return (
    <BookShelfContext.Provider value={ctx}>
      {children}
    </BookShelfContext.Provider>
  )
}