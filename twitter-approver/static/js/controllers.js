'use strict';

/* Controllers */

var tweetCheckControllers = angular.module('tweetCheckControllers', []);

tweetCheckControllers.controller('AuthorizeCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.getRequestToken = function() {
      $http.get('/auth/request').success(function(data, status, headers, config) {
        window.location.href = data.authorizationUrl;
      });
    };
}]);

tweetCheckControllers.controller('TweetListCtrl', ['$scope', 'Tweet',
  function($scope, Tweet) {
    $scope.tweets = Tweet.query();

    $scope.approveTweet = function(tweet) {
      tweet.approved = true;
      Tweet.update({tweetId:tweet.id}, tweet);
    };
}]);

tweetCheckControllers.controller('ComposeCtrl', ['$scope', 'Handle', 'Tweet',
  function($scope, Handle, Tweet) {
    $scope.handles = Handle.query();
    $scope.create = function(newTweet) {
      Tweet.save(newTweet);
    };
}]);
