// メールアドレスを Base64 エンコード
const encodedEmail = "ZnJlZXNlbXQra2Fubm9uX3F1ZXJ5QGdtYWlsLmNvbQ==";

// ボタンのクリックイベントでメールクライアントを起動
document.getElementById("contactButton").addEventListener("click", function () {
  const email = atob(encodedEmail); // Base64 をデコード
  const subject = encodeURIComponent("観音台の羽成公園・集会所のページについて"); // 件名を設定
  const body = encodeURIComponent("有志連絡係さんへ\n\n意見・提案・質問の内容：\n\n\n"); // 本文を設定
  const timestamp = new Date().getTime(); // 現在のタイムスタンプを取得
  window.location.href = `mailto:${email}?subject=${subject}&body=${body}&t=${timestamp}`; // クエリパラメータを追加
});

function showEmailImage() {
  const emailImageContainer = document.getElementById("emailImageContainer");
  emailImageContainer.style.display = "block";
}