# pspeed
## PageSpeed Insights API
Выборка по загрузке сайтов с помощью утилиты PageSpeed Insights API (PSI). Эта утилиты позволяет получать отчеты о скорости загрузки страниц на мобильных устройствах и компьютерах. 
PSI предоставляет данные о том, насколько быстро страница загружалась у настоящих пользователей. После того как дается задание проанализировать страницу по определенному URL, 
выполняется поиск сведений о ней в отчете об удобстве пользования браузером Chrome. В отчет PSI включаются доступные данные по показателям первой отрисовки контента (FCP), первой задержки 
ввода (FID) для всего источника или конкретной страницы с указанным URL, время загрузки самого большого визуального элемента сайта. 
Данные о фактической скорости загрузки в PSI обновляются ежедневно и охватывают последние 30 дней. 
Источник - https://developers.google.com/speed/docs/insights/v5/about?hl=ru

Краткое описание метрик:
- FIRST_CONTENTFUL_PAINT_MS - первая отрисовка контента. Измеряет, сколько времени требуется для визуализации исходного содержимого DOM, но не фиксирует,
  сколько времени потребовалось для визуализации самого большого (обычно более значимого) содержимого на странице
- FIRST_INPUT_DELAY_MS - Время ожидания для первого взаимодействия с контентом.
- LARGEST_CONTENTFUL_PAINT_MS - скорость загрузки основного контента. Измеряет время, за которое становится видимым самый большой элемент контента в области просмотра.

Возможно просмотреть и записать данный как по одному сайту, так и по всей группе порталов. Предусмотрен просмотр последних результата показателя LCP по всей группе сайтов. 
Параметр LARGEST_CONTENTFUL_PAINT_MS - скорость загрузки основного контента. Измеряет время, за которое становится видимым самый большой элемент контента в области просмотра. 
Точки относятся к 75 процентилю. Хороший результат считается при LCP меньше 2500 мс, неудовлетворительный - больше 4000 мс. Источник https://web.dev/lcp/

В базе данных хранятся адреса сайтов. В неё же записываются результаты, полученные от PSI. API_KEY для PSI хранится в config.json. Формат: 
`{
    "API_KEY": {
      "key": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }
}`