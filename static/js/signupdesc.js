$(document).ready(function () {
  $(".multi_select").selectpicker();
  var count=5;
  var values = $('#members').val(); 
  if (values.length > count) {
      // how many items we need to remove
      var toRemove = values.length - count;
      $('#members option:selected').each(function (index, item) {
        if (toRemove) {
          var option = $(item);
          option.prop('selected', false);
          toRemove--;
        }
      });
  }
  $('.selectpicker').selectpicker('refresh');
});

