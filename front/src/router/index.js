import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 * 此处路由每个角色都可以访问
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '主页', icon: 'dashboard' }
    }]
  },
  {
    path: '/front_user',
    component: () => import('@/views/front_information/front_index'),
    redirect: '/front_user/information',
    children: [
      {
        path: 'information',
        component: () => import('@/views/front_information/information'),
      }
    ]
  },
  {
    path: '/survey_mobile',
    component: () => import('@/views/front_information/information/survey_mobile'),
  },
  {
    path: '/front_myself',
    component: ()=>import('@/views/front_myself/information'),
    hidden: true,
    redirect: '/front_myself/Register_user',
    meta: { title: '信息收集页面预览', icon: 'el-icon-user-solid' },
    children: [
      {
        path: 'Register_user',
        component: () => import('@/views/front_myself/information/Register_user'),
        meta: { title: '基础信息', icon: 'el-icon-user-solid' }
      },
      {
        path: 'questionnaire',
        component: () => import('@/views/front_myself/information/questionnaire'),
        meta: { title: '问卷集合', icon: 'el-icon-user-solid' }
      },
      {
        path: 'read_text',
        component: () => import('@/views/front_myself/information/read_text'),
        meta: { title: '朗读页面预览', icon: 'el-icon-user-solid' }
      },
      {
        path: 'interview',
        component: () => import('@/views/front_myself/information/interview'),
        meta: { title: '访谈页面预览', icon: 'el-icon-user-solid' }
      },
      {
        path: 'other_page',
        component: () => import('@/views/front_myself/information/other'),
        meta: { title: '其他页面', icon: 'el-icon-user-solid' }
      }
    ]
  },
]
/**
 * 根据role动态构建路由
 */
export const asyncRoutes = [
  {
    path: '/manage',
    component: Layout,
    name: '系统管理',
    alwaysShow: true,
    meta: {
      title: '系统管理',
      icon: 'el-icon-s-tools',
      menu: 'system-manage'
    },
    redirect: '/manage/users',
    children: [
      {
        path: 'users',
        component: () => import('@/views/user/userList'),
        meta: { title: '用户管理', icon: 'el-icon-user-solid', menu: 'user-manage' }
      },
      {
        path: '/user/modify_self',
        component: () => import('@/views/user/editSelf'),
        meta: { title: '修改用户信息' },
        hidden: true
      },
      {
        path: '/user/add',
        component: () => import('@/views/user/userAdd'),
        meta: { title: '新增用户', menu: 'user-add' },
        hidden: true
      },
      {
        path: 'records',
        component: () => import('@/views/record/recordList'),
        meta: { title: '操作记录', icon: 'el-icon-postcard', menu: 'record-manage' }
      }]
  },
  {
    path: '/file_manage',
    component: layout,
    name: '信息采集管理',
    alwaysShow: true,
    meta: {
      title: '信息采集管理',
      icon: 'el-icon-folder',
      menu: 'system-manage'
    },
    redirect: '/file_manage/questionnaire_file_list',
    children: [
      {
        path: 'questionnaire_file_list',
        component: () => import('@/views/questionnaire_manage/questionnaireList'),
        meta: { title: '结构化数据管理', icon: 'el-icon-document' }
      },
      {
        path: 'text_file_list',
        component: () => import('@/views/question_manage/questionList_langdu'),
        meta: { title: '文本管理', icon: 'el-icon-tickets' }
      },
      // {
      //   path: 'question_list',
      //   component: () => import('@/views/question_manage/questionList_interview'),
      //   meta: { title: '面试文本管理', icon: 'el-icon-user-solid' }
      // },
      {
        path: 'front_user_list',
        // 包含了用户的相关信息，文件路径，是否采集等相关信息
        component: () => import('@/views/front_user/userList'),
        meta: { title: '参与者基本信息', icon: 'el-icon-user-solid' }
      },
      // {
      //   path: 'front_user_question_list',
      //   // 包含了用户的相关信息，文件路径，是否采集等相关信息
      //   component: () => import('@/views/questionnaire_manage/questionnaire_sds'),
      //   meta: { title: '问卷收集清单SDS', icon: 'el-icon-document-copy' }
      // },
      {
        path: 'mutil_file_list',
        // 包含了用户的相关信息，文件路径，是否采集等相关信息
        component: () => import('@/views/file_manage/fileList'),
        meta: { title: '数据收集管理', icon: 'el-icon-collection' }
      }
    ]
  },
  {
    path: '/result_manage',
    component: layout,
    name: '结果管理',
    alwaysShow: true,
    meta: {
      title: '结果管理',
      icon: 'el-icon-s-data',
      menu: 'system-manage'
    },
    redirect: '/result_manage/result_list',
    children: [
      {
        path: 'result_list',
        component: () => import('@/views/result_manage/resultList'),
        meta: { title: '结果清单', icon: 'el-icon-user-solid' }
      }]
  },
  {
    path: '/model_manage',
    component: layout,
    name: '模型管理',
    alwaysShow: true,
    meta: {
      title: '模型管理',
      icon: 'el-icon-menu',
      menu: 'system-manage'
    },
    redirect: '/model_manage/model_list',
    children: [
      {
        path: 'model_train',
        component: () => import('@/views/model_manage/model_train_1'),
        meta: { title: '模型训练-结构化', icon: 'el-icon-cpu' }
      },
      {
        path: 'model_test_1',
        component: () => import('@/views/model_manage/model_test_1'),
        meta: { title: '模型测试-结构化', icon: 'el-icon-cpu' }
      },
      // {
      //   path: 'model_train_2',
      //   component: () => import('@/views/model_manage/model_train_2'),
      //   meta: { title: '模型训练-2', icon: 'el-icon-cpu' }
      // },
      //
      // {
      //   path: 'model_test_2',
      //   component: () => import('@/views/model_manage/model_test_2'),
      //   meta: { title: '模型测试-2', icon: 'el-icon-cpu' }
      // },
      // {
      //   path: 'model_list',
      //   component: () => import('@/views/model_manage/modelList'),
      //   meta: { title: '模型清单', icon: 'el-icon-cpu' }
      // }
    ]
  },
  // {
  //   path: '/front_manage',
  //   component: layout,
  //   name: '前端页面管理-lsy',
  //   alwaysShow: true,
  //   meta: {
  //     title: '前端页面管理-lsy',
  //     icon: 'el-icon-box',
  //     menu: 'system-manage'
  //   },
  //   redirect: '/front_manage/front_user_base_info',
  //   children: [
  //     {
  //       path: 'index',
  //       component: () => import('@/views/front_information/information/index'),
  //       meta: { title: '总模块', icon: 'el-icon-user-solid' }
  //     },
  //     {
  //       path: 'front_user_survey',
  //       component: () => import('@/views/front_information/information/survey_mobile'),
  //       meta: { title: '移动端问卷展示', icon: 'el-icon-mobile-phone' }
  //     }
  //   ]
  // },
  {
    path: '/front_data_show',
    component: layout,
    // redirect: '/front_data_show/Register_user',
    name:"信息收集页面预览",
    meta: { title: '信息收集页面预览', icon: 'el-icon-mobile-phone' },
    children: [
      {
        path: 'Register_user',
        component: () => import('@/views/front_myself/information/Register_user'),
        meta: { title: '基础信息', icon: 'el-icon-user-solid' }
      },
      {
        path: 'questionnaire',
        component: () => import('@/views/front_myself/information/questionnaire'),
        meta: { title: '问卷集合', icon: 'el-icon-document' }
      },
      {
        path: 'read_text',
        component: () => import('@/views/front_myself/information/read_text'),
        meta: { title: '朗读页面预览', icon: 'el-icon-mic' }
      },
      {
        path: 'interview',
        component: () => import('@/views/front_myself/information/interview'),
        meta: { title: '访谈页面预览', icon: 'el-icon-video-play' }
      }
      ]
  },
  // {
  //   path: '/data_manage',
  //   component: layout,
  //   name: '数据管理',
  //   alwaysShow: true,
  //   meta: {
  //     title: '数据管理',
  //     icon: 'el-icon-s-tools',
  //     menu: 'system-manage'
  //   },
  //   redirect: '/data_manage/data_list',
  //   children: [
  //     {
  //       path: 'data_list',
  //       // 显示所有的数据
  //       component: () => import('@/views/file_manage/fileList'),
  //       meta: { title: '数据清单', icon: 'el-icon-user-solid' }
  //     }]
  // },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
