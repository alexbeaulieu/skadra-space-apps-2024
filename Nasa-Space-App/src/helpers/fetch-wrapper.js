export const fetchWrapper = {
  get: request('GET'),
  post: request('POST'),
  form: request('POST', true),
  put: request('PUT'),
  delete: request('DELETE')
};

function request(method, form = false) {
  return (url, body) => {
    const requestOptions = {
      method
    };
    
    if (form) {
      requestOptions.body = body;
    } else if (body) {
      const headers = { 'Content-Type': 'application/json' }
      requestOptions.headers = headers;
      requestOptions.body = JSON.stringify(body);
    }
   
    return fetch(url, requestOptions).then(handleResponse);
  };
}

function handleResponse(response) {
  return response.text().then((text) => {
    const data = text && JSON.parse(text);

    if (!response.ok) {
      const error = data || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
