var app = angular.module("wpApp", []);

app.controller("wpController", function($scope, $http) {

  $scope.words = [];

  $scope.addWord = function(w) {
    var d = {};
    d.word = w;
    $http.get("api/v1").then(function(response) {
      response.data.methods
        .filter((o) => o.name == "addWord")
        .forEach(function(o) {
          $http({
            method: ( typeof o.method === "undefined" ? "POST" : o.method ),
            url: o.url,
            data: d
          }).then(function(response) {
            $scope.words.push(response.data.word)
          });
        });
    });
  };

  $scope.removeWord = function(o) {
    o.methods.filter((o) => o.name == "delete")
      .forEach(function(m) {
        $http({
          method: ( typeof m.method === "undefined" ? "POST" : m.method ),
          url: m.url,
          data: o
        }).then(function(response) {
          var i = $scope.words.indexOf(o);
          $scope.words.splice(i, 1);
        });
      });
  };

  $scope.wordDidChange = function(o) {
    o.spinner = true;
  };

  $http.get("api/v1").then(function(response) {
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
