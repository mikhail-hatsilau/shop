(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductDetailsController", ProductDetailsController);

  ProductDetailsController.$inject = ['$scope', '$stateParams', 'Api', 'users'];

  function ProductDetailsController($scope, $stateParams, Api, users) {
    $scope.product = Api.products.get({id: $stateParams.id});
  }
})();
