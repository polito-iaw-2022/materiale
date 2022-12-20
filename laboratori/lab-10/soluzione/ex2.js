const books = [
    {
        id: 1,
        title: 'Il Signore degli Anelli',
        author: 'J.R.R. Tolkien',
        publicationDate: dayjs('1954-07-29'), // usando la libreria day.js
        averageReview: 5
    },
    {
        id: 2,
        title: '1984',
        author: 'George Orwell',
        publicationDate: dayjs('1949-06-08'),
        averageReview: 4.5
    },
    {
        id: 3,
        title: 'Moby Dick',
        author: 'Herman Melville',
        publicationDate: dayjs('1851-10-18')
    },
    {
        id: 4,
        title: 'Cime Tempestose',
        author: 'Emily Brontë',
        publicationDate: dayjs('1847-12-30'),
        averageReview: 3
    }
];

// Definizione della funzione aggiungiLibro
function aggiungiLibro(book) {
    // Controllo che il libro abbia tutte le proprietà obbligatorie
    if (book.id && book.title && book.author && book.publicationDate) {
        // Aggiungo il libro all'array di libri
        books.push(book);
    } else {
        console.log('Il libro non ha tutte le proprietà obbligatorie e non può essere aggiunto');
    }
}
// Definizione della funzione cancellaLibro
function cancellaLibro(book) {
    // Controllo che il libro sia presente nell'array di libri
    const bookIndex = books.findIndex(b => b.id === book.id);
    if (bookIndex !== -1) {
        // Rimuovo il libro dall'array di libri
        books.splice(bookIndex, 1);
    } else {
        console.log('Il libro non è presente nell\'array e non può essere cancellato');
    }
}
// Definizione della funzione calcolaMedia
function calcolaMedia() {
    // Calcolo la somma delle recensioni di tutti i libri
    const totalReviews = books.reduce((acc, book) => acc + (book.averageReview || 0), 0);
    // Calcolo la media delle recensioni
    return totalReviews / books.length;
}
// Definizione della funzione ritardaPubblicazione
function ritardaPubblicazione(days) {
    // Modifico la data di pubblicazione di tutti i libri presenti nell'array
    books.forEach(book => book.publicationDate = book.publicationDate.add(days, 'day'));
}
// Invocazione delle funzioni
aggiungiLibro({
    id: 5,
    title: 'Il Grande Gatsby',
    author: 'F. Scott Fitzgerald',
    publicationDate: dayjs('1925-04-10')
});
console.log(books)
cancellaLibro({ id: 2 });
console.log(books)
console.log(calcolaMedia()); // stampa la media delle recensioni di tutti i libri
ritardaPubblicazione(7); // sposta la data di pubblicazione di tutti i libri in avanti di 7 giorni
console.log(books)