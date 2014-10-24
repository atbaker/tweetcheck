'use strict';

// App module
var tweetCheckApp = angular.module('tweetCheckApp', [
  'ngRoute',
  'tweetCheckControllers',
  'tweetCheckFilters',
  'tweetCheckServices'
]);

tweetCheckApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/', {
        templateUrl: 'static/partials/tweet-list.html',
        controller: 'TweetListCtrl'
    }).
    otherwise({redirectTo: '/'});
}]);

tweetCheckApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
