import axios from 'axios';
import Cookies from 'js-cookie';

import schema from './schema.json';

function getCSRFToken() {
  // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
  return Cookies.get('csrftoken');
}

// create axios instance with custom config, or use default
const axiosApi = axios.create({
  withCredentials: true,
  headers: {
    'X-CSRFToken': getCSRFToken(),
  },
});

// helper method to substitute coerced url parameters
// e.g. url=/api/1/getTest/{id}/, kwargs={id: 1} => /api/1/getTest/1/
function createUrlFromKwargs(url, kwargs) {
  return Object.entries(kwargs)
    .reduce(
      (result, [key, value]) => result.replace(`{${key}}`, value),
      url,
    );
}

// create an object from the schema, whose attributes are the feature names
// these attributes are functions, which will call the endpoint
// through the pre-filled url and http method.
// NOTE an extra config argument { kwargs: Object } can be used to substitute url parameters not in query string
// e.g. await api.getTest({ kwargs: { id: 1 }});
// e.g. await api.listTests();
const api = Object.entries(schema).reduce(
  (acc, [feature, {method, url}]) => (
    ({kwargs = {}, ...config}) => axiosApi({
      url: createUrlFromKwargs(url, kwargs),
      method,
      ...config,
    })
  ),
  {},
);

export default api;