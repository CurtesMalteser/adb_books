import "./Book.css";


function Ratings(rating: number) {
    switch (true) {
        case (rating < 0.3): return <span className="fullStyled">☆☆☆☆☆</span>
        case (rating >= 0.3 && rating < 0.8): return <span className="fullStyled"><i className="halfStyled" data-content="★">☆</i>☆☆☆☆</span>
        case (rating >= 0.8 && rating < 1.3): return <span className="fullStyled">★☆☆☆☆</span>
        case (rating >= 1.3 && rating < 1.8): return <span className="fullStyled">★<i className="halfStyled" data-content="★">☆</i>☆☆☆</span>
        case (rating >= 1.8 && rating < 2.3): return <span className="fullStyled">★★☆☆☆</span>
        case (rating >= 2.3 && rating < 2.8): return <span className="fullStyled">★★<i className="halfStyled" data-content="★">☆</i>☆☆</span>
        case (rating >= 2.8 && rating < 3.3): return <span className="fullStyled">★★★☆☆</span>
        case (rating >= 3.3 && rating < 3.8): return <span className="fullStyled">★★★<i className="halfStyled" data-content="★">☆</i>☆</span>
        case (rating >= 3.8 && rating < 4.3): return <span className="fullStyled">★★★★☆</span>
        case (rating >= 4.3 && rating < 4.8): return <span className="fullStyled">★★★★<i className="halfStyled" data-content="★">☆</i></span>
        case (rating <= 5): return <span className="fullStyled">★★★★★</span>
    }
}

function RatingsCount(rating: number, ratingsCount: number) {
    return (
        <>
            <span>{rating} </span>
            {Ratings(rating)}
            <span> / </span>
            <span> {ratingsCount} ratings</span>
        </>
    )
}


function NoRatings() {
    return <span>No ratings yet</span>
}

function BookRating({ rating, ratingsCount }: { rating: number, ratingsCount: number }) {
    return (
        <div className="book-rating">
            {rating ? RatingsCount(rating, ratingsCount) : NoRatings()}
        </div>
    );
}

export default BookRating;