'use strict';

/* Controllers */

var tweetCheckControllers = angular.module('tweetCheckControllers', []);

tweetCheckControllers.controller('TweetListCtrl', ['$scope', 'Tweet',
  function($scope, Tweet) {
    $scope.tweets = Tweet.query();
    $scope.foo = 'bar';

    $scope.approveTweet = function(tweetId) {
      Tweet.approve({tweetId:tweetId});
    };
}]);
