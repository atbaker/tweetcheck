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
      templateUrl: 'static/partials/tweet-list.html',
      controller: 'TweetListCtrl'
    }).
    when('/compose', {
      templateUrl: 'static/partials/compose.html',
      controller: 'ComposeCtrl'
    }).
    when('/authorize', {
      templateUrl: 'static/partials/authorize.html',
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
