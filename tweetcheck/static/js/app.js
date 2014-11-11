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

tweetCheckApp.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

tweetCheckApp.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
