// Telegram WebApp SDK init
if (window.Telegram && window.Telegram.WebApp) {
  window.Telegram.WebApp.expand();
}

const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
const currentUserId = tg && tg.initDataUnsafe && tg.initDataUnsafe.user
  ? tg.initDataUnsafe.user.id
  : null;

// ফ্যালব্যাক: টেস্ট করার সময় ম্যানুয়ালি ID
// const currentUserId = 123456789;
