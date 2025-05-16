// デバイスがタッチデバイスかどうかを判定
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

// グローバルスコープで `today` を定義
const today = new Date();

// グローバルスコープでメッセージを定義
const DEFAULT_RESERVATION_MESSAGE = `日付を${isTouchDevice ? "タップ" : "クリック"}すると予約内容が表示されます。`;

// 昨日の日付を計算して挿入
function insertYesterdayDate() {
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const formattedDate = `${yesterday.getFullYear()}-${String(yesterday.getMonth() + 1).padStart(2, '0')}-${String(yesterday.getDate()).padStart(2, '0')}`;
  const yesterdayElement = document.getElementById('yesterday-date');
  if (yesterdayElement) {
    yesterdayElement.textContent = formattedDate;
  }
}

// キャッシュバスターを適用
function applyCacheBuster() {
  addCacheBusterToElement('js-core-min');
  addCacheBusterToElement('js-hall-reserve');
  addCacheBusterToElement('js-checkpw');
}

// 予約内容に基づいてアイコンを取得する関数
function getReservationIcon(reservation) {
  const keywordsToIcons = {
    "サロン": "🪑", // サロンのアイコン
    "クラブ": "🌺", // クラブのアイコン
    "体操": "👭", // 体操のアイコン
    "カフェ": "🍵", // カフェのアイコン
    "イベント": "🎉", // イベントのアイコン
  };

  // 予約内容が配列の場合、最初の一致するアイコンを返す
  if (Array.isArray(reservation)) {
    for (const item of reservation) {
      for (const [keyword, icon] of Object.entries(keywordsToIcons)) {
        if (item.includes(keyword)) {
          return icon;
        }
      }
    }
  }

  // 予約内容がオブジェクトの場合、値をチェック
  if (typeof reservation === "object" && reservation !== null) {
    for (const value of Object.values(reservation)) {
      for (const [keyword, icon] of Object.entries(keywordsToIcons)) {
        if (value.includes(keyword)) {
          return icon;
        }
      }
    }
  }

  // 予約内容が文字列の場合、キーワードに一致するアイコンを返す
  if (typeof reservation === "string") {
    for (const [keyword, icon] of Object.entries(keywordsToIcons)) {
      if (reservation.includes(keyword)) {
        return icon;
      }
    }
  }

  // デフォルトのアイコン
  return "✏️";
}

// カレンダーの初期化
function initializeCalendar() { 
  // サンプル予約データ
  let sampleReservations = {};

  // JSONデータをフェッチ（キャッシュバスターを追加）
  fetch(`scripts/calendar-reservations.json?v=${generateCacheBuster()}`)
    .then(res => res.json())
    .then(data => {
      sampleReservations = data;
      renderCalendar(currentYear, currentMonth);
      showReservationDetailForDate(today);
    })
    .catch(err => console.error('Error fetching reservations:', err));

  const minDate = new Date(today.getFullYear() - 1, today.getMonth(), 1);
  const maxDate = new Date(today.getFullYear() + 1, today.getMonth(), 1);

  let currentYear = today.getFullYear();
  let currentMonth = today.getMonth();
  let detailMode = false; // 詳細表示モードのフラグ
  let selectedDate = new Date(today); // 初期値は今日

  function pad(n) {
    return n < 10 ? '0' + n : n;
  }

  function showReservationDetailForDate(date) {
    const dateStr = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
    const res = sampleReservations[dateStr];
    let detail;
    if (Array.isArray(res)) {
      // 各予約を <div> で囲み、行を変えて表示
      detail = `<strong>${dateStr}</strong><br>` + res.map(item => `<div>${item}</div>`).join('');
    } else if (typeof res === 'object' && res !== null) {
      // 各時間帯ごとに <div> で囲み、行を変えて表示
      detail = `<strong>${dateStr}</strong><br>` +
        Object.entries(res).map(
          ([time, val]) =>
            `<div style="display:flex;gap:0.5em;">
             <span style="min-width:3em;font-weight:bold;text-align:left;">${time}</span>
             <span style="flex:1;text-align:left;">${val}</span>
           </div>`
        ).join('');
    } else if (typeof res === 'string') {
      detail = `<strong>${dateStr}</strong><br>${res}`;
    } else {
      detail = `<strong>${dateStr}</strong><br>予約はありません。`;
    }
    document.getElementById('reserveDetail').innerHTML = detail;
  }

  function renderCalendar(year, month) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDay = firstDay.getDay();
    const daysInMonth = lastDay.getDate();

    document.getElementById('currentMonth').textContent = `${year}年${month + 1}月`;

    const tbody = document.getElementById('calendarTable').querySelector('tbody');
    tbody.innerHTML = '';
    let tr = document.createElement('tr');
    for (let i = 0; i < startDay; i++) {
      tr.appendChild(document.createElement('td'));
    }
    for (let d = 1; d <= daysInMonth; d++) {
      const dateObj = new Date(year, month, d);
      const dateStr = `${year}-${pad(month + 1)}-${pad(d)}`;
      const td = renderDayCell(dateObj, dateStr);
      tr.appendChild(td);
      if ((startDay + d) % 7 === 0 || d === daysInMonth) {
        tbody.appendChild(tr);
        tr = document.createElement('tr');
      }
    }
  }

  function renderDayCell(date, dateStr) {
    const td = document.createElement('td');
    const holidayName = JapaneseHolidays.isHoliday(date);
    const res = sampleReservations[dateStr];
    const isReserved = !!res;

    if (!detailMode) {
      if (holidayName) {
        td.classList.add(isReserved ? 'holiday-reserved' : 'holiday');
        td.title = isReserved
          ? `${holidayName}／予約あり`
          : holidayName;
        td.innerHTML = `${date.getDate()}<br>
        <span>${holidayName}</span>`;
        if (isReserved) {
          td.innerHTML += `<br><span class="icon">${getReservationIcon(res)}</span>`;
        }
      } else if (isReserved) {
        td.classList.add('reserved');
        td.title = "予約あり";
        td.innerHTML = `${date.getDate()}<br><span class="icon">${getReservationIcon(res)}</span>`;
      } else {
        td.textContent = date.getDate();
      }
    } else {
      let reservationHtml = '';
      if (res) {
        if (Array.isArray(res)) {
          reservationHtml = res.join('<br>');
        } else if (typeof res === 'object') {
          reservationHtml = Object.entries(res)
            .map(([key, value]) => `${key}: ${value}`)
            .join('<br>');
        } else {
          reservationHtml = res;
        }
      }

      if (holidayName) {
        td.classList.add(isReserved ? 'holiday-reserved' : 'holiday');
        td.title = isReserved
          ? `${holidayName}／${reservationHtml.replace(/<[^>]+>/g, '')}`
          : holidayName;
        td.innerHTML = `${date.getDate()}<br>
        <span>${holidayName}</span>`;
        if (isReserved) {
          td.innerHTML += `<br><span class="reservation">${reservationHtml}</span>`;
        }
      } else if (isReserved) {
        td.classList.add('reserved');
        td.title = reservationHtml.replace(/<[^>]+>/g, '');
        td.innerHTML = `${date.getDate()}<br><span class="reservation">${reservationHtml}</span>`;
      } else {
        td.textContent = date.getDate();
      }
    }

    if (
      date.getFullYear() === selectedDate.getFullYear() &&
      date.getMonth() === selectedDate.getMonth() &&
      date.getDate() === selectedDate.getDate()
    ) {
      td.classList.add('selected');
    }

    td.onclick = () => {
      selectedDate = new Date(date);
      renderCalendar(currentYear, currentMonth);
      showReservationDetailForDate(date);
    };

    return td;
  }

  function changeMonth(diff) {
    let y = currentYear;
    let m = currentMonth + diff;
    if (m < 0) { y--; m = 11; }
    if (m > 11) { y++; m = 0; }
    const newDate = new Date(y, m, 1);
    if (newDate < minDate || newDate > maxDate) return;
    currentYear = y;
    currentMonth = m;
    renderCalendar(currentYear, currentMonth);
    document.getElementById('reserveDetail').innerHTML = DEFAULT_RESERVATION_MESSAGE; // 一元化されたメッセージを使用
  }

  document.getElementById('prevMonth').onclick = () => changeMonth(-1);
  document.getElementById('nextMonth').onclick = () => changeMonth(1);
  document.getElementById('goToday').onclick = () => {
  const wasDifferentMonth = currentYear !== today.getFullYear() || currentMonth !== today.getMonth();

  // 「今日」の年月に変更
  currentYear = today.getFullYear();
  currentMonth = today.getMonth();
  selectedDate = new Date(today); // 「今日」を選択状態に設定

  // カレンダーを再描画
  renderCalendar(currentYear, currentMonth);

  // 選択状態で予約情報を表示
  showReservationDetailForDate(selectedDate);
};
  document.getElementById('toggleDetail').addEventListener('click', () => {
    detailMode = !detailMode;
    document.getElementById('toggleDetail').textContent = detailMode ? '簡易表示' : '詳細表示';
    renderCalendar(currentYear, currentMonth);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  insertYesterdayDate();
  applyCacheBuster();
  initializeCalendar();
});