# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm install`

Installs all the dependencies required to run the project.

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

# Book Management APP

### Home `/`

Displays three shelves:
- Currently Reading
- Want to Read
- Read

Each shelf displays the books that belong to that category.

Each book displays the title, author(s), and a thumbnail of the book, a details button that links to the book details page, and a dropdown menu that allows the user to move the book to a different shelf.

### Search `/search`

Displays a search bar that allows the user to search for books.

The search results are displayed in a grid format, each book displays the title, author(s), and a thumbnail of the book, a details button that links to the book details page, and a dropdown menu that allows the user to move the book to a different shelf.

If the book is already on a shelf, the dropdown menu will display the shelf it belongs to.

When the user navigates back to the home page, the books that were added to a shelf will be displayed in the corresponding shelf.

### Book Details `/book/:id`

Displays the book details, including the title, author(s), description, rating, category, publisher, puplished date, pages count, ISBN-13 and ISBN-10.

If some of the details, such as the rating, category, publisher, published date, pages count, ISBN-13, or ISBN-10 are not available, the page is correctly displayed.

The user can search for terms like "poetry" and "biography". It is possible to search for multiple words, such as “artificial intelligence.”

### Thanks and credits
Thank you to React, React Bootstrap, and React Router for making this project possible.

Thank you to the Udacity team for providing the API server.

Special thank you to Maximilian Schwarzmüller, for the extra curricular and companion course which helped me understand React better: *React - The Complete Guide 2024 (incl. React Router & Redux)*. 

Also, thank you to the authors of the books that are displayed in the app.