(function(){
	'use strict'

	var app = angular.module("shopApp", ['ui.router', 'ngResource']);

	app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider){
		
		$urlRouterProvider.otherwise('products');

		$stateProvider.
			state("products", {
				url: "/products",
				templateUrl: "/static/templates/products.html",
				controller: "ProductsController",
			}).
			state("details", {
				url: "/products/:id",
				templateUrl: "/static/templates/product-details.html",
				controller: "ProductDetailsController"
			}).
			state("orders", {
				url: "/orders",
				templateUrl: "static/templates/orders.html",
				controller: "OrdersController"
			});
	}]);

	app.config(["$resourceProvider", function($resourceProvider){
		$resourceProvider.defaults.stripTrailingSlashes = false;
	}]);
})();