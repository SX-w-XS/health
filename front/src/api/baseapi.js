// import request from 'request'
import request from '@/utils/request'
import axios from 'axios'
// const base = `http://localhost:8080`;
// const base = ``

export const encodeQueryParams=(params) =>{
  const query = Object.keys(params)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&');
  return `?${query}`;
}

export const postRequest = (url, params) => {
  return request({
    method: 'POST',
    url: `${url}`,
    data: params
  })
}

export const postRequest_multipart = (url, params) => {
  return request({
    method: 'POST',
    url: `${url}`,
    data: params,
    headers: {
      'Content-Type': 'multipart/form-data'
    },
  })
}

export const getRequest = (url, params) => {
  return request({
    method: 'GET',
    url: `${url}`,
    data: params
  })
}

export const putRequest = (url, params) => {
  return request({
    method: 'PUT',
    url: `${url}`,
    data: params
  })
}

export const delRequest = (url, params) => {
  return request({
    method: 'delete',
    url: `${url}`,
    data: params
  })
}


export const postRequestDownload_axios = (url, params) => {
  return  axios({
    method: "POST",
    url: `${url}`,
    data: params,
    responseType: 'blob', // 设置响应类型为二进制数据
  })
}

//模型训练
export const getModelTrain_axios = (url, params) => {
  return axios({
    method: "GET",
    url: `${url}`,
    data:params
  })
}
