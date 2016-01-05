(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.factory("Api", ApiFactory);

  ApiFactory.$inject = ['$resource', '$http'];

  function ApiFactory($resource, $http){

    var api = {
      products: function(token){
        return $resource("/api/v1/products/:id", {id: '@id'}, {
          update: {
            method: 'PUT',
            headers: {
              'X-CSRFToken': token
            }
          },

          query: {
            method: 'GET',
            transformResponse: function (data, headersGetter) {
                var jsonData = angular.fromJson(data);
                angular.forEach(jsonData.objects, function(item, index){
                  jsonData.objects[index] = new (api.products(token))(item);
                });
                return jsonData;
              },
            isArray: false,
          },

          save: {
            method: 'POST',
            headers: {
              'X-CSRFToken': token
            }
          },

          delete: {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': token
            }
          }
          
        });
      },
      orders: function(token){
        return $resource("/api/v1/orders/:id", {id: '@id'}, {
          update: {
            method: 'PUT',
            headers: {
              'X-CSRFToken': token
            }
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

          save: {
            method: 'POST',
            headers: {
              'X-CSRFToken': token
            }
          },

          delete: {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': token
            }
          }

        })
      },
      users: function(token){
        return $resource("/api/v1/users/:id", {id: '@id'}, {
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
            headers: {
              'X-CSRFToken': token
            }
          },

          save: {
            method: 'POST',
            headers: {
              'X-CSRFToken': token
            }
          },

          delete: {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': token
            }
          }
        })
      },
      categories: function(token){
        return $resource('/api/v1/categories/:id', {id: '@id'}, {
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
            headers: {
              'X-CSRFToken': token
            }
          },

          save: {
            method: 'POST',
            headers: {
              'X-CSRFToken': token
            }
          },

          delete: {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': token
            }
          }
        })
      },
    };

    return api;

  }


})();
