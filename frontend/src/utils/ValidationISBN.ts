function splitListByIndex(list: Array<number>) {
    const evenList = Array<number>()
    const oddList = Array<number>()

    list.forEach((item, index) => {
        if (index % 2 === 0) {
            evenList.push(item)
        } else {
            oddList.push(item)
        }
    })

    return { evenList, oddList }
}

function validateISBN13(isbn: any[]): boolean {
    let validationDigit = isbn.pop()

    const { evenList, oddList } = splitListByIndex(isbn)

    const evenResult = evenList.reduce((acc, current) => acc + current, 0)
    const oddResult = oddList.reduce((acc, current) => acc + (current * 3), 0)
    const sum = evenResult + oddResult
    return (10 - (sum % 10)) === validationDigit
}

function validateISBN10(isbn: any[]): boolean {
    let validationDigit = isbn.pop()

    const sum = isbn.map((item, index) => (index + 1) * item)
        .reduce((sum, current) => sum + current, 0)

    const remainder = sum % 11
    let checkDigit = remainder === 10 ? 'X' : remainder
    return checkDigit === validationDigit
}

export function validateISBN(isbn: any[]) {
    switch (isbn.length) {
        case 13:
            return validateISBN13(isbn)
        case 10:
            return validateISBN10(isbn)
        default:
            return false
    }
}