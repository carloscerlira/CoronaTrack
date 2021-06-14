$(document).ready(function(){
    $.ajaxSetup({ cache: false });
    $('#search').keyup(function(){
     $('#result').html('');
     $('#state').val('');
     var searchField = $('#search').val();
     var expression = new RegExp(searchField, "i");
     if (searchField == ''){ return }
     $.getJSON('https://raw.githubusercontent.com/carloscerlira/CoronaTrack/mexico/data/mexico/general.json', function(data) {
      $.each(data, function(key, value){
       if (value.country.search(expression) != -1)
       {
        var url = 'href=country/'+value.iso+' '
        var flag = '<img src = https://www.countryflags.io/'+value.iso+'/shiny/32.png> '
        $('#result').append('<a '+url+'class="list-group-item list-group-item-action">'+ flag + value.country + '</a>');
       }
      });   
     });
    });
   });