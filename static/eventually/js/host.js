document.addEventListener('DOMContentLoaded', function() {
    var date_picker = document.querySelectorAll('.datepicker');
    var time_picker = document.querySelectorAll('.timepicker');
    var instances = M.Datepicker.init(date_picker, {
        'showClearBtn': true,
        'minDate': new Date()});
    instances = M.Timepicker.init(time_picker, {
        'showClearBtn': true,
        'fromNow': 5000,
        'twelveHour': false});
  });