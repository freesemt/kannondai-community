// 現在の日付を基にキャッシュバスターを生成する関数
function generateCacheBuster() {
  const today = new Date();
  return `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`;
}

// キャッシュバスターをURLに追加する関数
function addCacheBusterToElement(id, attribute = 'src', extra = '') {
  const element = document.getElementById(id);
  if (element) {
    const originalUrl = element.getAttribute(attribute);
    if (originalUrl) {
      const cleanUrl = originalUrl.split('?')[0]; // 既存のクエリパラメータを削除
      element.setAttribute(attribute, `${cleanUrl}?v=${generateCacheBuster()}${extra}`);
    }
  }
}

/**
 * 指定されたリンクにキャッシュバスターを付ける
 * @param {string[]} links - キャッシュバスターを付けたいリンクの配列
 */
function addCacheBusterToLinks(links, extra = '') {
  links.forEach(link => {
    const anchor = document.querySelector(`a[href="${link}"]`);
    if (anchor) {
      anchor.href = `${link}?v=${generateCacheBuster()}${extra}`;
    }
  });
}

// キャッシュバスターを追加してスクリプトを読み込む
function addScriptWithCacheBuster(id, src, extra = "") {
  const script = document.createElement('script');
  script.id = id;
  script.src = `${src}?v=${generateCacheBuster()}${extra}`;
  document.head.appendChild(script);
}