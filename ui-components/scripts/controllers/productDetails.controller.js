(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductDetailsController", ProductDetailsController);

  ProductDetailsController.$inject = ['$scope', '$stateParams', 'Api'];

  function ProductDetailsController($scope, $stateParams, Api) {
    $scope.product = Api.products.get({id: $stateParams.id});
  }
})();
