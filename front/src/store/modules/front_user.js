
const getDefaultState = () => {
  return {
    register_user: {
      "username": "string",
      "gender": "string",
      "age": "string",
      "location": "string",
      "level": "string",
      "email": "string",
      "is_active": "未完成",
      "is_person_questionare": "未完成",
      "is_mental_questionare": "未完成",
      "is_read_audio": "未完成",
      "is_read_video": "未完成",
      "is_interview_audio": "未完成",
      "is_interview_video": "未完成",
      "is_send_mail": "未完成",
      "mental_status": "无",
      "is_delete": 0,
      "id": 1,
    }
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_register_user: (state, register_user) => {
    state.register_user = register_user
  }
}

const actions = {
  set_register_user(context, user) {
    context.commit('SET_register_user', user);
  }
}
export default {
  namespaced: true,
  state,
  mutations,
  actions
}

