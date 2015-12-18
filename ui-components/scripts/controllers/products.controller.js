(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductsController", ProductsController);

  ProductsController.$inject = ['$scope', 'Api', 'users', '$uibModal'];

  function ProductsController($scope, Api, users, $uibModal){
    $scope.categories = Api.categories.query();
    $scope.products = Api.products.query();

    $scope.addToCart = addToCart;
    $scope.openAddNewPopup = openAddNewPopup;

    function addToCart(product){
      var order = new Api.orders();

      order.user = users[0].resource_uri;
      order.product = product.resource_uri;
      order.date = new Date();

      order.$save(function(){
        product.inOrder = true;
      });
    }

    function openAddNewPopup(){
      var modalInstance,
          params = {
            animation: true,
            templateUrl: 'static/templates/new-product.html',
            controller: 'NewProductController',
            resolve: {
              users: function(){
                return users;
              },
              productsCategories: function(){
                return $scope.categories;
              }
            }
          }

      modalInstance = $uibModal.open(params);
      modalInstance.result.then(function(product){
        $scope.products.push(product);
      });
    }

  }

})();
