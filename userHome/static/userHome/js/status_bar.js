$(document).ready(function() {
    $('input[type="radio"]').change(function() {
      $('.line').removeClass('line-active'); // Remove active class from all lines
  
      var selectedValue = $(this).val();
      if (selectedValue === 'verified') {
        $('.line.line-1').addClass('line-active');
      } else if (selectedValue === 'completed') {
        $('.line.line-1, .line.line-2').addClass('line-active');
      }
    });
  
    // Trigger change event for initial selection
    $('input[type="radio"]:checked').change();
  });
  