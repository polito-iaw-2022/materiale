'use strict;'

document.querySelectorAll('aside > .filtri-data > ul > li > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    document.querySelectorAll('aside > .filtri-data > ul > li > a').forEach((link) => link.classList.remove('active'));
    const filter = e.target.dataset.fildate;
    const articles = document.querySelectorAll('article');
    for (let article of articles) {
      const data_pubblicazione = dayjs(article.dataset.pubdate);
      e.target.classList.add('active');
      article.classList.add('hide');
      if (filter == 'oggi' && dayjs().diff(data_pubblicazione, 'day') < 1)
        article.classList.remove('hide');
      else if (filter == 'settimana' && dayjs().diff(data_pubblicazione, 'week') < 1)
        article.classList.remove('hide');
      else if (filter == 'mese' && dayjs().diff(data_pubblicazione, 'month') < 1)
        article.classList.remove('hide');
      else if (filter == 'tutti')
        article.classList.remove('hide');
    }
  });
});

document.querySelectorAll('aside > .filtri-ordine > ul > li > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    document.querySelectorAll('aside > .filtri-ordine > ul > li > a').forEach((link) => link.classList.remove('active'));
    e.target.classList.add('active');
    let articles = document.querySelectorAll('[data-pubdate]');
    let arrayIndexes = Array.from(articles);

    let sorted = arrayIndexes.sort(comparator);
    if (e.target.dataset.filordine == 'discendente')
      sorted.reverse();
    sorted.forEach(e =>
      document.querySelector('#lista-posts').appendChild(e));
  });
});

function comparator(a, b) {
  let dataA = dayjs(a.dataset.pubdate);
  let dataB = dayjs(b.dataset.pubdate);
  if (dataA.isBefore(dataB, 'day'))
    return -1;
  if (dataA.isAfter(dataB, 'day'))
    return 1;
  return 0;
}