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
