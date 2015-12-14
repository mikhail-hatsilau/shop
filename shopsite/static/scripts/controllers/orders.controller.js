(function(){

	var app = angular.module("shopApp");

	app.controller("OrdersController", OrdersController);

	OrdersController.$inject = ['$scope', 'Api'];

	function OrdersController($scope, Api){
		$scope.orders = Api.orders.query();

		$scope.removeOrder = removeOrder;

		function removeOrder(order){
			order.$delete(function(){
				orderIndex = $scope.orders.indexOf(order);
				$scope.orders.splice(orderIndex, 1);
			});
		}
	}
})()