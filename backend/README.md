# adb_books API

### setup instructions
Set the following in your .env (Flask):
```
REACT_APP_API_SERVER_URL=http://localhost:3000
REACT_APP_AUTH0_DOMAIN=<auth0_domain - provided to the reviewer in the review notes>
REACT_APP_AUTH0_CLIENT_ID=<auth0_client - provided to the reviewer in the review notes>
REACT_APP_AUTH0_CALLBACK_URL=http://localhost:3000/callback
REACT_APP_AUTH0_AUDIENCE=<app_audience - provided to the reviewer in the review notes>
DB_PATH=<path_to_sqlite_db>
REDIS_HOST=<redis_host>
REDIS_PORT=<redis_port>
REDIS_PASSWORD=<redis_password>
```

- **Note:** `DB_PATH` and `REDIS_HOST/PORT/PASSWORD` are require for local development. The API is deployed and instrucions will be provided in the review notes. As well, the Auth0 domain, client ID, and audience are provided in the review notes.
- Postman and API URL will be provided in the review notes.

### Running the Backend

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Create a virtual environment
```bash
python3 -m venv .venv
```

#### Activate the virtual environment
```bash
source .venv/bin/activate
```

#### Run the Flask application
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --debugger --reload
```

#### Run tests
```bash
pytest --cov=app --cov-report=html
```    

Or if do not want to generate the HTML report:

```bash
pytest --cov=app
```

## API Documentation

### Authorization
All endpoints require a valid JWT token provided by Auth0. Include it in the `Authorization` header: 

`Authorization: Bearer <your_token_here>`

---

### `GET /booklist/<string:shelf>`
**Description:** Retrieve a list of books from a specific shelf.
**Path Parameters:**
- `shelf`: The shelf to retrieve books from (`currently-reading`, `to-read`, `read`).
**Permissions:** `booklist:get`  
**Response:**
```json
{
    "books": [
        {
            "authors": [
                "Stephen King"
            ],
            "image": "https://images.isbndb.com/covers/25111313482781.jpg",
            "isbn10": null,
            "isbn13": "9781668089330",
            "shelf": null,
            "title": "Never Flinch: A Novel"
        }
    ],
    "limit": 20,
    "page": 1,
    "success": true,
    "total_results": 1
}
```

---

### `GET /search/books?q=George%20Orwell&limit=2`
**Description:** Retrieve a list of all books in the database.  
**Permissions:** `booklist:get`  
**Response:**
```json
{
    "books": [
        {
            "authors": [
                "George ORWELL"
            ],
            "date_published": "2022",
            "image": "https://images.isbndb.com/covers/25357393484343.jpg",
            "isbn": "605511433X",
            "isbn13": "9786055114336",
            "language": "en",
            "msrp": 0.0,
            "pages": 96,
            "publisher": "2022",
            "rating": 0.0,
            "subjects": [
                "Subjects"
            ],
            "subtitle": "Animal Farm - New - by George Orwell",
            "synopsis": "The description of Animal Farm Book: Overworked and mistreated animals one day gather and take over the farm where they live. They finally have a say, determined to create a more just and equal society on the farm. They begin to work to establish this new order under the leadership of the pigs. Although this order helped the farm to develop at first, problems that the animals could not foresee will arise over time and a more brutal regime will be established than before. Animal Farm is George Orwell's second well-known modern classic novel and a striking political satire. One of the best critiques of the system ever written, this novel reveals how a liberation revolution can evolve into one-manhood. George Orwell's allegory remains relevant today in every situation and place where freedom is attacked.",
            "title": "Animal Farm - New - by George Orwell"
        },
        {
            "authors": [
                "George Orwell"
            ],
            "date_published": "1949",
            "image": "https://images.isbndb.com/covers/20750443484344.jpg",
            "isbn": "605746222X",
            "isbn13": "9786057462220",
            "language": "en",
            "msrp": 0.0,
            "publisher": "1949",
            "rating": 0.0,
            "subjects": [
                "Subjects"
            ],
            "subtitle": "1984 George Orwell - Nineteen Eighty-Four - Paperback",
            "synopsis": "Newspeak, Doublethink, Big Brother, the Thought Police - the language of 1984 has passed into the English language as a symbol of the horrors of totalitarianism. George Orwell's story of Winston Smith's fight against the all-pervading Party has become a classic, not the least because of its intellectual coherence. First published in 1949, it retains as much relevance today as it had then.",
            "title": "1984 George Orwell - Nineteen Eighty-Four - Paperback"
        }
    ],
    "limit": "2",
    "page": 1,
    "success": true,
    "total_results": 5547
}
```

---

### `GET /search/shelves?q=golden`
**Description:** This endpoint allows you to search for books across all shelves based on a query string. It returns a list of books that match the search criteria.
**Query Parameters:**
- `q`: The search query string.
**Permissions:** `booklist:get`
**Response:**
```json
{
    "books": [
        {
            "authors": [
                "John C. Wright"
            ],
            "image": "https://images.isbndb.com/covers/10055843482299.jpg",
            "isbn10": null,
            "isbn13": "9780312848705",
            "shelf": null,
            "title": "The Golden Age"
        }
    ],
    "limit": 20,
    "page": 1,
    "success": true,
    "total_results": 1
}
```

---

### `POST /curated-list`
**Description:** Add a curated list of books.
**Permissions:** `booklist:curator`
**Request Body:**
```json
{
    "name": "Neurodiversity",
    "description": "A list of books that explore the concept of neurodiversity."
}
```
**Response:**
```json
{
    "success": true,
    "list": {
        "name": "Neurodiversity",
        "description": "A list of books that explore the concept of neurodiversity.",
        "id": 1
    }
}
```

---

### `PUT /curated-lists
**Description:** Update a curated list of books.
**Permissions:** `booklist:curator`
**Request Body:**
```json
{
    "id": 1,
    "name": "Neurodiversity Updated",
    "description": "An updated list of books that explore the concept of neurodiversity."
}
```
**Response:**
```json
{
    "success": true,
    "list": {
        "id": 1,
        "name": "Neurodiversity Updated",
        "description": "An updated list of books that explore the concept of neurodiversity."
    }
}
```

---

### `DELETE /curated-list/<int:list_id>`
**Description:** Delete a curated list of books.
**Path Parameters:**
- `list_id`: The ID of the curated list to delete.
**Permissions:** `booklist:curator`
**Status Code** 204 No Content (indicates successful deletion)

---

### `GET /curated-lists`
**Description:** Fetches curated lists of books.
**Permissions:** `booklist:get`
**Response:**
```json
{
    "lists": [
        {
            "id": 1,
            "name": "Neurodiversity",
            "description": "A list of books that explore the concept of neurodiversity."
        }
    ],
    "success": true
}
```

---

### `POST /curated-pick`
**Description:** Add a book to a curated list.
**Permissions:** `booklist:curator`
**Request Body:** At least one of `isbn13` or `isbn10` must be provided.
```json
{
    "list_id": 1,
    "isbn13": "9780393609646",
    "isbn10": "0393609642",
    "position": 1
}
```
**Response:**
```json
{
    "pick": {
        "id": 1,
        "isbn13": "9780393609646",
        "list_id": 1,
        "position": 1
    },
    "success": true
}
```

---

### `DELETE /curated-pick/<int:pick_id>`
**Description:** Remove a book from a curated list.
**Path Parameters:**
- `pick_id`: The ID of the pick to delete.
**Permissions:** `booklist:curator`
**Status Code:** 204 No Content (indicates successful deletion)

---
### `PATCH /curated-pick/<string:pick_id>`
**Description:** Update the book position in a curated list.
**Path Parameters:**
- `pick_id`: The ID of the pick to update. Either `isbn10` or `isbn13`.
**Permissions:** `booklist:curator`
**Request Body:**
```json
{
    "position": 2
}
```
**Response:**
```json
{
    "pick": {
        "id": 1,
        "isbn13": "9780393609646",
        "list_id": 1,
        "position": 2
    },
    "success": true
}
```

---

### `GET /curated-picks/<int:list_id>`
**Description:** Fetches all picks from a curated list.
**Path Parameters:**
- `list_id`: The ID of the curated list.
**Permissions:** `booklist:get`
**Response:**
```json
{
    "books": [
        {
            "authors": [
                "Edith Sheffer"
            ],
            "date_published": "2018-05-01",
            "image": "https://images.isbndb.com/covers/3177343482328.jpg",
            "isbn": "0393609642",
            "isbn13": "9780393609646",
            "language": "en",
            "msrp": 27.95,
            "pages": 320,
            "position": 1,
            "publisher": "2018-05-01",
            "rating": 0.0,
            "shelf": null,
            "subjects": [
                "Health, Fitness & Dieting",
                "Psychology & Counseling",
                "History",
                "Children's Health",
                "Autism & Asperger's Syndrome",
                "Europe",
                "World",
                "Jewish",
                "Medical Books",
                "Psychology",
                "Specialty Boutique",
                "New, Used & Rental Textbooks"
            ],
            "subtitle": "",
            "synopsis": "Shortlisted for the 2019 Mark Lynton History Prize<br/><br/>A groundbreaking exploration of the chilling history behind an increasingly common diagnosis.<br/>Hans Asperger, the pioneer of autism and Asperger syndrome in Nazi Vienna, has been celebrated for his compassionate defense of children with disabilities. But in this groundbreaking book, prize-winning historian Edith Sheffer exposes that Asperger was not only involved in the racial policies of Hitler’s Third Reich, he was complicit in the murder of children.<br/>As the Nazi regime slaughtered millions across Europe during World War Two, it sorted people according to race, religion, behavior, and physical condition for either treatment or elimination. Nazi psychiatrists targeted children with different kinds of minds―especially those thought to lack social skills―claiming the Reich had no place for them. Asperger and his colleagues endeavored to mold certain \"autistic\" children into productive citizens, while transferring others they deemed untreatable to Spiegelgrund, one of the Reich’s deadliest child-killing centers.<br/>In the first comprehensive history of the links between autism and Nazism, Sheffer uncovers how a diagnosis common today emerged from the atrocities of the Third Reich. With vivid storytelling and wide-ranging research, Asperger’s Children will move readers to rethink how societies assess, label, and treat those diagnosed with disabilities. 15 illustrations",
            "title": "Asperger's Children: The Origins of Autism in Nazi Vienna"
        }
    ],
    "limit": 1,
    "page": 1,
    "success": true,
    "total_results": 1
}
```

---
### `GET /ny-times/best-sellers/fiction`
### `GET /ny-times/best-sellers/non-fiction`
**Description:** Fetches the New York Times Best Sellers list for fiction or non-fiction.
**Permissions:** `booklist:get`
**Response:**
```json
{
    "books": [
        {
            "authors": [
                "Navessa Allen"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781638932253.jpg",
            "isbn10": "",
            "isbn13": "9781638932253",
            "title": "CAUGHT UP"
        },
        {
            "authors": [
                "V.E. Schwab"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781250320520.jpg",
            "isbn10": "",
            "isbn13": "9781250320520",
            "title": "BURY OUR BONES IN THE MIDNIGHT SOIL"
        },
        {
            "authors": [
                "Taylor Jenkins Reid"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780593158715.jpg",
            "isbn10": "",
            "isbn13": "9780593158715",
            "title": "ATMOSPHERE"
        },
        {
            "authors": [
                "Bill Clinton and James Patterson"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780316565103.jpg",
            "isbn10": "",
            "isbn13": "9780316565103",
            "title": "THE FIRST GENTLEMAN"
        },
        {
            "authors": [
                "Carley Fortune"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780593638910.jpg",
            "isbn10": "",
            "isbn13": "9780593638910",
            "title": "ONE GOLDEN SUMMER"
        },
        {
            "authors": [
                "Stephen King"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781668089330.jpg",
            "isbn10": "",
            "isbn13": "9781668089330",
            "title": "NEVER FLINCH"
        },
        {
            "authors": [
                "Sarah J. Maas"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781639736447.jpg",
            "isbn10": "",
            "isbn13": "9781639736447",
            "title": "HOUSE OF FLAME AND SHADOW"
        },
        {
            "authors": [
                "Wally Lamb"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781668006399.jpg",
            "isbn10": "",
            "isbn13": "9781668006399",
            "title": "THE RIVER IS WAITING"
        },
        {
            "authors": [
                "Freida McFadden"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781464227318.jpg",
            "isbn10": "",
            "isbn13": "9781464227318",
            "title": "THE TENANT"
        },
        {
            "authors": [
                "Riley Sager"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780593472408.jpg",
            "isbn10": "",
            "isbn13": "9780593472408",
            "title": "WITH A VENGEANCE"
        },
        {
            "authors": [
                "Ali Hazelwood"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9798217187430.jpg",
            "isbn10": "",
            "isbn13": "9798217187430",
            "title": "PROBLEMATIC SUMMER ROMANCE"
        },
        {
            "authors": [
                "Emily Henry"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780593441299.jpg",
            "isbn10": "",
            "isbn13": "9780593441299",
            "title": "GREAT BIG BEAUTIFUL LIFE"
        },
        {
            "authors": [
                "Michael Connelly"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9780316588485.jpg",
            "isbn10": "",
            "isbn13": "9780316588485",
            "title": "NIGHTSHADE"
        },
        {
            "authors": [
                "Navessa Allen"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781638932239.jpg",
            "isbn10": "",
            "isbn13": "9781638932239",
            "title": "LIGHTS OUT"
        },
        {
            "authors": [
                "S.A. Cosby"
            ],
            "image": "https://static01.nyt.com/bestsellers/images/9781250832061.jpg",
            "isbn10": "",
            "isbn13": "9781250832061",
            "title": "KING OF ASHES"
        }
    ],
    "limit": 15,
    "page": 1,
    "success": true,
    "total_results": 15
}
```

---

### `POST /book`
**Description:** Add a book to a specific shelf.
**Permissions:** `book:add_to_shelf`
**Request Body:**
```json
{
    "authors": [ "Fernando Pessoa" ],
    "image": "https://images.isbndb.com/covers/12/19/9789723711219.jpg",
    "isbn13": "9789723711219",
    "shelf": "want-to-read",
    "title": "LIVRO DO DESASSOSSEGO"
}
```
**Response:**
```json
{
    "book": {
        "authors": [
            "Fernando Pessoa"
        ],
        "image": "https://images.isbndb.com/covers/12/19/9789723711219.jpg",
        "isbn13": "9789723711219",
        "shelf": "want-to-read",
        "title": "LIVRO DO DESASSOSSEGO"
    },
    "success": true
}
```

---

### `GET /book/<string:book_id>`
**Description:** Retrieve a book by its isbn10 or isbn13.
**Path Parameters:**
- `book_id`: The isbn10 or isbn13 of the book to retrieve.
**Permissions:** `book:get_details`
**Response:**
```json
{
    "book": {
        "authors": [
            "Freida McFadden"
        ],
        "date_published": "2023-07-11",
        "image": "https://images.isbndb.com/covers/7779693482312.jpg",
        "isbn": "0349132615",
        "isbn13": "9780349132617",
        "language": "en",
        "msrp": 0.0,
        "pages": 352,
        "publisher": "2023-07-11",
        "rating": 0.0,
        "shelf": null,
        "subjects": [
            "Fiction, thrillers, psychological",
            "Fiction, thrillers, domestic"
        ],
        "subtitle": "The Housemaid's Secret",
        "synopsis": "As he continues showing me their incredible penthouse apartment, I have a terrible feeling about the woman behind closed doors. But I can't risk losing this job – not if I want to keep my darkest secret safe . . .<br/>It's hard to find an employer who doesn't ask too many questions about my past. So I thank my lucky stars that the Garricks miraculously give me a job, cleaning their stunning penthouse with views across the city and preparing fancy meals in their shiny kitchen. I can work here for a while, stay quiet until I get what I want. It's almost perfect. But I still haven't met Mrs Garrick, or seen inside the guest bedroom. I'm sure I hear her crying. I notice spots of blood around the neck of her white nightgowns when I'm doing laundry. And one day I can't help but knock on the door. When it gently swings open, what I see inside changes everything....<br/>That's when I make a promise. After all, I've done this before. I can protect Mrs. Garrick while keeping my own secrets locked up safe. Douglas Garrick has done wrong. He is going to pay. It's simply a question of how far I'm willing to go....<br/>An unbelievably twisty read that will have you glued to the pages late into the night. Anyone who loves The Woman in the Window, The Wife Between Us and The Girl on the Train will be completely hooked!",
        "title": "The Housemaid's Secret"
    },
    "success": true
}
```

---
### `DELETE /book/<string:book_id>`
**Description:** Remove a book from a specific shelf.
**Path Parameters:**
- `book_id`: The isbn10 or isbn13 of the book to remove.
**Permissions:** `book:delete_shelf`
**Response:**
```json
{
    "deleted": "9780349132617",
    "success": true
}
```

---
### `PATCH /book/<string:book_id>`
**Description:** Update a book's shelf.
**Path Parameters:**
- `book_id`: The isbn10 or isbn13 of the book to update.
**Permissions:** `book:update_shelf`
**Request Body:**
- `shelf`: The destination shelf: one of `currently-reading`, `to-read`, or `read`.
```json
{
    "shelf": "read"
}
```
**Response:**
```json
{
    "success": true
}
``` 