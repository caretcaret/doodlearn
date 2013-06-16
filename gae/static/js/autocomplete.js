$(document).ready(function() {

  $.getJSON( '/search/ajax', {
    test: 'doesntmatterjustfortest'
  })
  .done(function( data ) {
    $("#tags").autocomplete({
        source: data
    });
  });
});
