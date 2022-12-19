'use strict;'

document.querySelectorAll('section > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const filter = e.target.dataset.tag;
    const articles = document.querySelectorAll('article');
    for (let article of articles) {
      if(filter !== 'all' && filter !== article.querySelector('.tag > a').text)
        article.classList.add('hide');
      else
        article.classList.remove('hide');
    }
  });
});