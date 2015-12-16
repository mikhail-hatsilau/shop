(function(){
	'use strict'

	var app = angular.module("shopApp");

	app.factory("Api", ApiFactory);

	ApiFactory.$inject = ['$resource', '$http'];

	function ApiFactory($resource, $http){

		var api = {
			products: $resource("/api/v1/products/:id", {id: '@id'}, {
				update: {
					method: 'PUT'
				},

				query: {
					method: 'GET',
					transformResponse: $http.defaults.transformResponse.concat([
			            function (data, headersGetter) {
			                return data.objects;
			            }
			        ]),
					isArray: true,
				}
			}),
			orders: $resource("/api/v1/orders/:id", {id: '@id'}, {
				update: {
					method: 'PUT'
				},

				query: {
					method: 'GET',
					transformResponse: $http.defaults.transformResponse.concat([
			            function (data, headersGetter) {
			                return data.objects;
			            }
			        ]),
					isArray: true,
				}
			}),
			users: $resource("/api/v1/users/:id", {id: '@id'}, {
				query: {
					method: 'GET',
					transformResponse: $http.defaults.transformResponse.concat([
			            function (data, headersGetter) {
			                return data.objects;
			            }
			        ]),
					isArray: true,
				}
			}),
		};

		return api;

	}


})();