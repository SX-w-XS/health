import request from '@/utils/request'

export function getList(pageNo, skip, limit) {
  return request({
    url: '/back/model_file_records',
    method: 'get',
    params: { skip: 0,
      limit: 50
    }
  })
}
