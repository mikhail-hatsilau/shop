(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("ProductsController", ProductsController);

  ProductsController.$inject = ['$scope', 'Api', '$rootScope', '$uibModal', '$cacheFactory', 'localStorageService'];

  function ProductsController($scope, Api, $rootScope, $uibModal, $cacheFactory, localStorageService){

    var cache = $cacheFactory.get('productsCache'),
        selectedKey = 'selectedItem';

    $scope.maxPageSize = 5;

    if (angular.isUndefined(cache)){
      cache = $cacheFactory('productsCache');
    } 

    $scope.categories = Api.categories.query(function(){
      if ($scope.categories){
        $scope.selected = localStorageService.get(selectedKey);
        if (angular.isUndefined($scope.selected) || $scope.selected === null){
          setSelected();
        } else {
          if (!categoryExists($scope.selected, $scope.categories)) {
            setSelected();
          }
        }
        loadProducts();
      }
    });

    function setSelected() {
      $scope.selected = $scope.categories[0];
      localStorageService.set(selectedKey, $scope.selected);
    }

    function categoryExists(obj, array) {
      var element = _.find(array, function(item) {
        return item.id === obj.id;
      });

      if (!element) {
        return false;
      }

      return true;
    }

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

    $scope.addToCart = addToCart;
    $scope.openAddNewPopup = openAddNewPopup;
    $scope.pageChanged = pageChanged;
    $scope.updateCategory = updateCategory;

    function addToCart(product){
      var order = new Api.orders();
      order.user = $rootScope.user.resource_uri;
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
              user: function(){
                return $rootScope.user;
              },
              productsCategories: function(){
                return $scope.categories;
              }
            }
          }

      modalInstance = $uibModal.open(params);
      modalInstance.result.then(function(product){
        if ($scope.products.length < $scope.meta.limit && $scope.selected.id === product.category.id){
          $scope.products.push(product);
        }
        $scope.meta.totalCount++;
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
      localStorageService.set(selectedKey, $scope.selected);
      loadProducts();
    }

  }

})();
