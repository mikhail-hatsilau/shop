(function(){

  var app = angular.module("shopApp");

  app.controller("OrdersController", OrdersController);

  OrdersController.$inject = ['$scope', 'Api', 'users'];

  function OrdersController($scope, Api, users){
    $scope.orders = Api.orders.query();

    $scope.removeOrder = removeOrder;

    function removeOrder(order){
      order.$delete(function(data){
        orderIndex = $scope.orders.indexOf(order);
        $scope.orders.splice(orderIndex, 1);
      });
    }
  }
})();
