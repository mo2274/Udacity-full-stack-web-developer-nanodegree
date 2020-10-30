/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-mohamed.us', // the auth0 domain prefix
    audience: 'CoffeeShopApi', // the audience set for the auth0 app
    clientId: 'S9FMy4CkkFS8DL96A4FkvEf4aoAFCw0z', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
