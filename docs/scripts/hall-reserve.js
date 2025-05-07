document.addEventListener('DOMContentLoaded', function() {
  let sampleReservations = {};

  // fetch('sample-reservations.json')
  fetch('scripts/calendar-reservations.json')
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

  function pad(n) { return n < 10 ? '0' + n : n; }

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

    if (isReserved) {
      if (detailMode) {
        // 詳細表示
        // 予約内容を複数行で表示（今のまま）
        let reservationHtml = '';
        if (Array.isArray(res)) {
          reservationHtml = res.map(item =>
            `<div style="font-size:0.8em;" class="calendar-reserve-item">${item}</div>`
          ).join('');
        } else if (typeof res === 'object' && res !== null) {
          reservationHtml = Object.entries(res)
            .map(([time, val]) =>
              `<div style="font-size:0.8em;" class="calendar-reserve-item">${time}:${val}</div>`
            ).join('');
        } else if (typeof res === 'string') {
          reservationHtml = `<span style="font-size:0.8em;" class="calendar-reserve-item">${res}</span>`;
        }

        if (holidayName && isReserved) {
          td.classList.add('holiday-reserved');
          td.title = `${holidayName}／${reservationHtml.replace(/<[^>]+>/g, '')}`;
          td.innerHTML = `${date.getDate()}<br>
            <span style="font-size:0.8em;">${holidayName}</span><br>
            ${reservationHtml}`;
        } else if (holidayName) {
          td.classList.add('holiday');
          td.title = holidayName;
          td.innerHTML = `${date.getDate()}<br><span style="font-size:0.8em;">${holidayName}</span>`;
        } else if (isReserved) {
          td.classList.add('reserved');
          td.title = reservationHtml.replace(/<[^>]+>/g, '');
          td.innerHTML = `${date.getDate()}<br>${reservationHtml}`;
        } else {
          td.textContent = date.getDate();
        }
      } else {
        // 簡易表示（鉛筆アイコンのみ）
        td.innerHTML = `${date.getDate()} <span class="reserve-icon" title="予約あり">✏️</span>`;
      }
    } else {
      td.textContent = date.getDate();
    }
    if (
      date.getFullYear() === today.getFullYear() &&
      date.getMonth() === today.getMonth() &&
      date.getDate() === today.getDate()
    ) {
      td.classList.add('today');
    }
    td.onclick = () => {
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
    renderCalendar(currentYear, currentMonth);
    document.getElementById('reserveDetail').innerHTML = "日付をクリックすると予約内容が表示されます。";
  };

  // トグルボタン
  document.getElementById('toggleDetail').addEventListener('click', () => {
    detailMode = !detailMode;
    document.getElementById('toggleDetail').textContent = detailMode ? '簡易表示' : '詳細表示';
    renderCalendar(currentYear, currentMonth);
  });
});