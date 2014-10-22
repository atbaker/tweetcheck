'use strict';

/* Services */

var tweetCheckServices = angular.module('tweetCheckServices', ['ngResource']);

tweetCheckServices.factory('Tweet', ['$resource',
  function($resource){
    return $resource('api/tweets/:tweetId', {}, {
      query: {method:'GET', isArray: false}
    });
}]);
