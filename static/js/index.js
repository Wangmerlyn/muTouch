window.HELP_IMPROVE_VIDEOJS = false;

function copyBibTeX() {
  const bibtexElement = document.getElementById('bibtex-code');
  const button = document.querySelector('.copy-bibtex-btn');
  const copyText = button ? button.querySelector('.copy-text') : null;

  if (!bibtexElement || !button || !copyText) {
    return;
  }

  const bibtexText = bibtexElement.textContent.trim();

  const markCopied = function () {
    button.classList.add('copied');
    copyText.textContent = 'Copied';
    setTimeout(function () {
      button.classList.remove('copied');
      copyText.textContent = 'Copy';
    }, 1800);
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(bibtexText).then(markCopied).catch(function () {
      const textArea = document.createElement('textarea');
      textArea.value = bibtexText;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      markCopied();
    });
    return;
  }

  const textArea = document.createElement('textarea');
  textArea.value = bibtexText;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);
  markCopied();
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', function () {
  const scrollButton = document.querySelector('.scroll-to-top');
  if (!scrollButton) {
    return;
  }

  if (window.pageYOffset > 280) {
    scrollButton.classList.add('visible');
  } else {
    scrollButton.classList.remove('visible');
  }
});

document.addEventListener('DOMContentLoaded', function () {
  if (window.bulmaCarousel) {
    bulmaCarousel.attach('.carousel', {
      slidesToScroll: 1,
      slidesToShow: 1,
      loop: true,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 4500
    });
  }
});
