(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductsController", ProductsController);

  ProductsController.$inject = ['$scope', 'Api', 'users'];

  function ProductsController($scope, Api, users){
    $scope.products = Api.products.query();

    $scope.addToCart = addToCart;

    function addToCart(product){
      var order = new Api.orders();

      order.user = users[0].resource_uri;
      order.product = product.resource_uri;
      order.date = new Date();

      order.$save(function(){
        product.inOrder = true;
      });
    }
  }

})();