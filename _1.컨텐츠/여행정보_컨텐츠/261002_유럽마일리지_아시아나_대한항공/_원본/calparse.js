() => {
  const wrap = document.querySelector('.flight_calendar_wrap');
  if (!wrap) return null;
  const dates = wrap.querySelectorAll('.inner_top span.date');
  const out = { period: dates[0] ? dates[0].innerText.trim() : '', asOf: dates[1] ? dates[1].innerText.trim() : '', days: {} };
  wrap.querySelectorAll('.fc-content-skeleton table').forEach(t => {
    const heads = [...t.querySelectorAll('thead tr td')];
    const cols = heads.map(td => td.getAttribute('data-date'));
    heads.forEach(td => {
      const d = td.getAttribute('data-date');
      if (d) out.days[d] = { cls: td.className.replace(/\s+/g, ' ').trim(), link: !!td.querySelector('a'), ev: [] };
    });
    t.querySelectorAll('tbody tr').forEach(tr => {
      [...tr.children].forEach((td, i) => {
        const d = cols[i];
        if (!d) return;
        td.querySelectorAll('a').forEach(a => out.days[d].ev.push(a.className.replace(/fc-[\w-]+/g, '').replace(/\s+/g, ' ').trim()));
      });
    });
  });
  return out;
}
