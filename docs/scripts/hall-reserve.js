document.addEventListener('DOMContentLoaded', () => {
  // 現在の日付を取得
  const today = new Date();

  // 昨日の日付を計算
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  // 日付をフォーマット（例: 2025-05-09）
  const formattedDate = `${yesterday.getFullYear()}-${String(yesterday.getMonth() + 1).padStart(2, '0')}-${String(yesterday.getDate()).padStart(2, '0')}`;

  // HTMLに挿入
  document.getElementById('yesterday-date').textContent = formattedDate;
});

document.addEventListener('DOMContentLoaded', () => {
  // 現在の日付を取得（例: 20250508）
  const today = new Date();
  const cacheBuster = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`;

  // キャッシュバスターを付与する関数
  function addCacheBuster(id) {
    const element = document.getElementById(id);
    if (element) {
      const srcOrHref = element.getAttribute('src') || element.getAttribute('href');
      if (srcOrHref) {
        const cleanUrl = srcOrHref.split('?')[0]; // 既存のクエリパラメータを削除
        element.setAttribute('src', `${cleanUrl}?v=${cacheBuster}`);
        element.setAttribute('href', `${cleanUrl}?v=${cacheBuster}`);
      }
    }
  }

  // 必要な要素にキャッシュバスターを付与
  // addCacheBuster('css-hall-reserve');
  addCacheBuster('js-core-min');
  addCacheBuster('js-hall-reserve');
  addCacheBuster('js-checkpw');
});

document.addEventListener('DOMContentLoaded', function() {
  let sampleReservations = {};

  // fetch('sample-reservations.json')
  fetch('scripts/calendar-reservations.json?v=2')
    .then(res => res.json())
    .then(data => {
      sampleReservations = data;
      renderCalendar(currentYear, currentMonth);
      showReservationDetailForDate(today);
    });

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

  const today = new Date();
  const minDate = new Date(today.getFullYear() - 1, today.getMonth(), 1);
  const maxDate = new Date(today.getFullYear() + 1, today.getMonth(), 1);

  let currentYear = today.getFullYear();
  let currentMonth = today.getMonth();
  let detailMode = false; // 追加: 詳細表示モードのフラグ
  let selectedDate = new Date(today); // 初期値は今日

  function pad(n) { return n < 10 ? '0' + n : n; }

  function renderCalendar(year, month) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDay = firstDay.getDay();
    const daysInMonth = lastDay.getDate();

    document.getElementById('currentMonth').textContent = `${year}年${month + 1}月`;
    // document.getElementById('currentYear').textContent = `${currentYear}年`;
    // document.getElementById('currentMonthOnly').textContent = `${currentMonth + 1}月`;

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

  console.log(`Date: ${dateStr}, Holiday: ${holidayName}, Reserved: ${isReserved}`);

  // 簡易表示モードの場合
  if (!detailMode) {
    if (holidayName) {
      td.classList.add(isReserved ? 'holiday-reserved' : 'holiday');
      td.title = isReserved
        ? `${holidayName}／予約あり`
        : holidayName;
      td.innerHTML = `${date.getDate()}<br>
        <span>${holidayName}</span>`;
      if (isReserved) {
        td.innerHTML += `<br><span class="icon">✏️</span>`; // 鉛筆アイコンを表示
      }
    } else if (isReserved) {
      td.classList.add('reserved');
      td.title = "予約あり";
      td.innerHTML = `${date.getDate()}<br><span class="icon">✏️</span>`; // 鉛筆アイコンを表示
    } else {
      td.textContent = date.getDate();
    }
  } else {
    // 詳細表示モードの場合
    let reservationHtml = '';
    if (res) {
      if (Array.isArray(res)) {
        reservationHtml = res.join('<br>');
      } else if (typeof res === 'object') {
        reservationHtml = Object.entries(res)
          .map(([key, value]) => `${key}: ${value}`)
          .join('<br>');
      } else {
        reservationHtml = res.toString();
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

  // 選択された日付の処理
  if (
    date.getFullYear() === selectedDate.getFullYear() &&
    date.getMonth() === selectedDate.getMonth() &&
    date.getDate() === selectedDate.getDate()
  ) {
    td.classList.add('selected');
  }

  // 日付クリック時の処理
  td.onclick = () => {
    selectedDate = new Date(date); // 選択日を更新
    renderCalendar(currentYear, currentMonth); // 再描画で.selectedが正しく付く
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
    document.getElementById('reserveDetail').innerHTML = "日付をクリックすると予約内容が表示されます。";
  }

  document.getElementById('prevMonth').onclick = () => changeMonth(-1);
  document.getElementById('nextMonth').onclick = () => changeMonth(1);
  document.getElementById('goToday').onclick = () => {
    currentYear = today.getFullYear();
    currentMonth = today.getMonth();
    selectedDate = new Date(today); // 選択日を今日に更新
    renderCalendar(currentYear, currentMonth);
    document.getElementById('reserveDetail').innerHTML = "日付をクリックすると予約内容が表示されます。";
  };

  // トグルボタン
  document.getElementById('toggleDetail').addEventListener('click', () => {
    detailMode = !detailMode;
    document.getElementById('toggleDetail').textContent = detailMode ? '簡易表示' : '詳細表示';
    renderCalendar(currentYear, currentMonth);
  });

  console.log(JapaneseHolidays.isHoliday(new Date(2025, 0, 1))); // 例: 元日
});