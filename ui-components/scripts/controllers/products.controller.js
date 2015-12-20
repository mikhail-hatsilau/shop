(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductsController", ProductsController);

  ProductsController.$inject = ['$scope', 'Api', 'users', '$uibModal', '$cacheFactory'];

  function ProductsController($scope, Api, users, $uibModal, $cacheFactory){

    var cache = $cacheFactory.get('productsCash');
    if (angular.isUndefined(cache)){
      cache = $cacheFactory('productsCash');
    } 

    $scope.categories = Api.categories.query(function(){
      if ($scope.categories){
        $scope.selected = cache.get('selectedCategory');
        if (angular.isUndefined($scope.selected)){
          $scope.selected = $scope.categories[0];
        }
        loadProducts();
      }
    });

    function loadProducts() {
      $scope.products = cache.get('products');
      $scope.meta = cache.get('meta');

      if (angular.isUndefined($scope.products) && angular.isUndefined($scope.meta)) {
        Api.products.query({
          category__id: $scope.selected.id
        }, function(data){
          $scope.products = data.objects;
          $scope.meta = data.meta;
          addToCache();
        });
      }
    }

    console.log($scope.products);
    console.log($scope.meta);

    $scope.addToCart = addToCart;
    $scope.openAddNewPopup = openAddNewPopup;
    $scope.pageChanged = pageChanged;
    $scope.updateCategory = updateCategory;

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
        addToCache();
      });
    }

    function pageChanged(){
      var offset = $scope.meta.limit * ($scope.currentPage - 1),
          limit = $scope.meta.limit
      Api.products.query({
        category__id: $scope.selected.id,
        limit: limit,
        offset: offset
      }, function(data){
        $scope.products = data.objects;
        $scope.meta = data.meta;
      });
    }

    function addToCache(){
      cache.put('products', $scope.products);
      cache.put('meta', $scope.meta);
    }

    function updateCategory(){
      cache.removeAll();
      cache.put('selectedCategory', $scope.selected);
      loadProducts();
    }

  }

})();
