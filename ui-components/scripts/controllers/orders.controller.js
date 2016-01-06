(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.controller("OrdersController", OrdersController);

  OrdersController.$inject = ['$scope', 'Api', '$cacheFactory'];

  function OrdersController($scope, Api, $cacheFactory){

    $scope.orders = Api.orders.query();

    $scope.removeOrder = removeOrder;

    function removeOrder(order){
      order.$delete(function(data){
        var cache = $cacheFactory.get('productsCache'),
            orderIndex;
        if (!angular.isUndefined(cache)) {
          cache.removeAll();
        }
        orderIndex = $scope.orders.indexOf(order);
        $scope.orders.splice(orderIndex, 1);
      });
    }
  }
})();
