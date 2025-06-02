// lang.js：自動語言偵測 + fallback 為英文

const supportedLanguages = ['en', 'zh-TW'];

// 先讀取使用者曾經切換的語言
let savedLang = localStorage.getItem('lang');

// 如果沒有儲存過，從瀏覽器語言自動判斷
if (!savedLang) {
  const browserLang = navigator.language || navigator.userLanguage;

  if (browserLang === 'zh-TW') {
    savedLang = 'zh-TW';
  } else {
    savedLang = 'en'; // 預設 fallback 英文
  }

  // 第一次使用時可以先不寫入 localStorage，等使用者切換後再儲存也可以
}

window.currentLang = savedLang;
document.documentElement.lang = currentLang;

// 切換語言函式
function setLang(lang) {
  if (supportedLanguages.includes(lang)) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    document.documentElement.lang = lang;
  }
}