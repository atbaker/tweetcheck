'use strict';

/* Controllers */

var tweetCheckControllers = angular.module('tweetCheckControllers', []);

var shortUrlLength = 22;
var shortUrlLengthHttps = 23;

tweetCheckControllers.controller('AuthorizeCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.getRequestToken = function() {
      $http.get('/auth/request').success(function(data, status, headers, config) {
        window.location.href = data.authorizationUrl;
      });
    };
}]);

tweetCheckControllers.controller('TweetListCtrl', ['$scope', 'Tweet', 'Handle',
  function($scope, Tweet, Handle) {
    $scope.handles = {};
    $scope.tweets = Tweet.query(function() {
      // Populate the handles object with details about each handle in these tweets
      for (var i=0; i<$scope.tweets.results.length; i++) {
        var handleId = $scope.tweets.results[i].handle;
        if (!$scope.handles.hasOwnProperty(handleId)) {
          $scope.handles[handleId] = Handle.query({handleId: handleId});
        }
      }
    });

    $scope.approveTweet = function(tweet) {
      tweet.approved = true;
      Tweet.update({tweetId:tweet.id}, tweet);
    };
}]);

tweetCheckControllers.controller('ComposeCtrl', ['$scope', 'Handle', 'Tweet',
  function($scope, Handle, Tweet) {
    $scope.handles = Handle.query();
    $scope.remainingCharacters = 140;

    $scope.updateCharacterCounter = function(body) {
      if (body === undefined) {
        $scope.remainingCharacters = 140;
        return;
      }
      var splitBody = body.split(' ');
      var remaining = 140;

      for (var i=0; i<splitBody.length; i++) {
        if (splitBody[i].substring(0, 7) === 'http://' && splitBody[i].length > shortUrlLength) {
          remaining -= shortUrlLength;
        } else if (splitBody[i].substring(0, 8) === 'https://' && splitBody[i].length > shortUrlLengthHttps) {
          remaining -= shortUrlLengthHttps;
        } else {
          remaining -= Math.max(splitBody[i].length, 1);
        }
      }
      $scope.remainingCharacters = remaining;
    };

    $scope.create = function(newTweet) {
      Tweet.save(newTweet);
      window.location.href = '/#';
    };
}]);
