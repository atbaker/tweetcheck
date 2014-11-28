'use strict';

// App module
var tweetCheck = angular.module('tweetCheck', [
  'ngRoute',
  'tweetCheckControllers',
  'tweetCheckFilters',
  'tweetCheckServices'
]);

tweetCheck.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/', {
      templateUrl: 'static/views/tweet-list.html',
      controller: 'TweetListCtrl'
    }).
    when('/compose', {
      templateUrl: 'static/views/compose.html',
      controller: 'ComposeCtrl'
    }).
    when('/authorize', {
      templateUrl: 'static/views/authorize.html',
      controller: 'AuthorizeCtrl'
    }).
    otherwise({redirectTo: '/'});
}]);

tweetCheck.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

tweetCheck.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
