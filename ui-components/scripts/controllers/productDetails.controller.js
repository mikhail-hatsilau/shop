(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductDetailsController", ProductDetailsController);

  ProductDetailsController.$inject = ['$scope', '$stateParams', 'Api', '$rootScope'];

  function ProductDetailsController($scope, $stateParams, Api, $rootScope) {
  	var token = $rootScope.token;
    $scope.product = Api.products(token).get({id: $stateParams.id});
  }
})();
