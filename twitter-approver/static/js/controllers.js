'use strict';

/* Controllers */

var tweetCheckControllers = angular.module('tweetCheckControllers', []);

tweetCheckControllers.controller('TweetListCtrl', ['$scope', 'Tweet',
  function($scope, Tweet) {
    $scope.tweets = Tweet.query();

    $scope.approveTweet = function(tweet) {
      tweet.approved = true;
      Tweet.update({tweetId:tweet.id}, tweet);
    };
}]);

tweetCheckControllers.controller('AuthorizeCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.getRequestToken = function() {
      $http.get('/auth/request').success(function(data, status, headers, config) {
        window.location.href = data.authorizationUrl;
      });
    };
}]);
