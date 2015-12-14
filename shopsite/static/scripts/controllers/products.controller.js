(function(){
	'use strict'

	var app = angular.module("shopApp");

	app.controller("ProductsController", ProductsController);

	ProductsController.$inject = ['$scope', 'Api'];

	function ProductsController($scope, Api){

		$scope.products = Api.products.query();

		$scope.addToCart = addToCart;

		function addToCart(product){
			var order = new Api.orders();

			order.user = "/api/v1/users/2/";
			order.product = product.resource_uri;
			order.date = new Date();

			order.$save(function(){
				product.inOrder = true;
			});
		}
	}

})();