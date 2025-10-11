(function () {
  function injectContent(root) {
    if (!root) return;
    fetch('assets/content/ai-seo-flow.txt', { cache: 'no-cache' })
      .then(function (response) {
        if (!response.ok) throw new Error('Failed to load shared content');
        return response.text();
      })
      .then(function (text) {
        root.textContent = text;
      })
      .catch(function (error) {
        console.error(error);
        root.textContent = '[コンテンツ読み込みエラー] ' + error.message;
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.querySelector('[data-shared-content]');
    injectContent(container);
  });
})();
