(function(document, window, $, config) {
  'use strict';

  var apiURL = 'https://api.flickr.com/services/rest/';

  $.getJSON("http://api.flickr.com/services/feeds/groups_pool.gne?id=" + config.apiKey + "@N22&lang=en-us&format=json&jsoncallback=?", function(data) {
    $.each(data.items, function(i, item){
      $("<img/>").attr("src", item.media.m).appendTo("#images")
      .wrap("<a href='" + item.link + "'></a>");
    });
  });
})(document, window, jQuery, config);
