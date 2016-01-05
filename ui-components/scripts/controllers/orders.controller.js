(function(){

  var app = angular.module("shopApp");

  app.controller("OrdersController", OrdersController);

  OrdersController.$inject = ['$scope', 'Api', '$cacheFactory', '$rootScope'];

  function OrdersController($scope, Api, $cacheFactory, $rootScope){
    var token = $rootScope.token;

    $scope.orders = Api.orders(token).query();

    $scope.removeOrder = removeOrder;

    function removeOrder(order){
      order.$delete(function(data){
        var cache = $cacheFactory.get('productsCache');
        if (!angular.isUndefined(cache)) {
          cache.removeAll();
        }
        orderIndex = $scope.orders.indexOf(order);
        $scope.orders.splice(orderIndex, 1);
      });
    }
  }
})();
