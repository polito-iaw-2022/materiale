'use strict';

const scores = [28, 25, 21, 30, 18, 24, 22];

console.log('Array originale: ' + scores.join(', '))

const copia_1 = [...scores]
const copia_2 = [...scores]

// trova il voto più alto
let min_pos = 0;
for (let i = 0; i < copia_1.length; i++) {
    if (copia_1[i] < copia_1[min_pos])
        min_pos = i;
}
// elimina il voto più alto
copia_1.splice(min_pos, 1)

// trova il voto più basso
min_pos = 0;
for (let i = 0; i < copia_1.length; i++) {
    if (copia_1[i] < copia_1[min_pos])
        min_pos = i;
}
// elimina il voto più basso
copia_1.splice(min_pos, 1)

console.log('Array senza il voto più alto e più basso: ' + copia_1.join(', '))

// calcola la media dell'array scores
let new_avg = 0;
for (let x of scores) {
    new_avg += x;
}
new_avg /= scores.length;

copia_2.splice(0, 0, Math.round(new_avg));
copia_2.splice(0, 0, Math.round(new_avg));

console.log('Array con due voti in testa uguali alla media: ' + copia_2.join(', '))