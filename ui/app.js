var app = angular.module("wpApp", []);

app.controller("wpController", function($scope, $http) {

  $scope.words = [];

  $scope.addWord = function(w) {
    var i = {};
    i.word = w;
    i.id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0,
        v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
    $scope.words.push(i);
  };

  $scope.removeWord = function(o) {
    var i = $scope.words.indexOf(o);
    $scope.words.splice(i, 1);
  };

  $scope.wordDidChange = function(o) {
    o.spinner = true;
  };

  $http.get("api.json").then(function(response) {
    response.data.methods
      .filter((o) => o.name == "getWords")
      .forEach(function(o) {
        $http({
          method: ( typeof o.method === "undefined" ? "GET" : o.method ),
          url: o.url
        }).then(function(response) {
          $scope.words = response.data.words;
          $scope.wordsDoneLoading = true;
        });
      });
  });

});
