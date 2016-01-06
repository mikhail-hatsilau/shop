(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.factory("Api", ApiFactory);

  ApiFactory.$inject = ['$resource', '$http'];

  function ApiFactory($resource, $http){

    var api = {
      products: $resource("/api/v1/products/:id", {id: '@id'}, {
        update: {
          method: 'PUT',
        },

        query: {
          method: 'GET',
          transformResponse: function (data, headersGetter) {
              var jsonData = angular.fromJson(data);
              angular.forEach(jsonData.objects, function(item, index){
                jsonData.objects[index] = new api.products(item);
              });
              return jsonData;
            },
          isArray: false,
        },
        
      }),
      orders: $resource("/api/v1/orders/:id", {id: '@id'}, {
        update: {
          method: 'PUT',
        },

        query: {
          method: 'GET',
          transformResponse: $http.defaults.transformResponse.concat([
            function (data, headersGetter) {
              return data.objects;
            }
          ]),
          isArray: true,
        },

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
        },

        update: {
          method: 'PUT',
        },
      }),
      loggedUser: $resource("/api/v1/users/logged/", {}, {
        get: {
          method: 'GET',
          transformResponse: function(data, headersGetter){
            var dataJson = angular.fromJson(data);
            return angular.fromJson(dataJson.user);
          }
        }
      }),
      categories: $resource('/api/v1/categories/:id', {id: '@id'}, {
        query: {
          method: 'GET',
          transformResponse: $http.defaults.transformResponse.concat([
            function (data, headersGetter) {
              return data.objects;
            }
          ]),
          isArray: true,
        },

        update: {
          method: 'PUT',
        },
      }),
    };

    return api;

  }


})();
