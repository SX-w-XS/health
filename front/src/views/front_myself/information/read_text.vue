<template>
  <div class="content">
    <el-tabs v-model="activeName" @tabComplete="switchToTab">
      <el-tab-pane label="用户协议" name="first" style="width: 100%">
        <User_contact  @go-to-next-tab="goToNextTab"></User_contact>
      </el-tab-pane>
      <el-tab-pane label="语音录入" name="audio" style="width: 100%">
        <Audio v-if="dataReady"   @go_to_next_menu="completeNextModel" :dataSource="texts_audio"   :user="now_user" :tablist="tab_list" :muilt_type="muilt_type" @go-to-next-tab="goToNextTab"></Audio>
      </el-tab-pane>
      <el-tab-pane label="视频录入" name="video" style="width: 100%">
        <Video v-if="dataReady"  @go_to_next_menu="completeNextModel" :dataSource="texts_video"  :user="now_user" :tablist="tab_list"  :muilt_type="muilt_type" @go-to-next-tab="goToNextTab"></Video>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>
<script>
// 题目接口
import { getRequest } from '@/api/baseapi'
import jsondata from '../../../static/API.json'
import questionnaire from '@/views/front_myself/information/component/Questionnaire'
import Audio from '@/views/front_myself/information/component/Audio'
import Audio2 from '@/views/front_myself/information/component/Audio2'
import user_contact from '@/views/front_myself/information/user_contact'

import Video from '@/views/front_myself/information/component/Video'
const modelApi = '/front/get_all2'
export default {
  name: 'read_text',
  data() {
    return {
      activeName: 'first',
      muilt_type:'text',
      dataReady:false,
      texts_audio: [],
      texts_video:[],
      tab_list: [],
      tab_list_emit: ['first','audio','video'],
      user: null
    }
  },
  methods: {
    goToNextTab() {
      if (this.activeName==='first') {
        this.activeName = this.tab_list_emit[1]
        return
      }
      if (this.activeName==='audio') {
        this.activeName = this.tab_list_emit[2]
        return
      }

    },
    completeNextModel() {
      this.$emit("go_to_next_menu")
    },
    switchToTab(tabName) {
      console.log(tabName)
      this.activeName = tabName;
    },
    init_data(){
      this.getRequest(modelApi).then(res => {
        if (res) {
          this.texts_audio = res.texts_audio
          this.texts_video = res.texts_video
        }
      })
      // this.questionnaires=jsondata.questionnaires
      console.log('打印json数据集')
      console.log(this.questionnaires)
      console.log('打印json数据集长度')
      console.log(this.questionnaires.length)
      console.log('打印子集')
      console.log(this.questionnaires[0])
      // this.activeName="tab_"+this.questionnaires[0].id
    }
  },
  computed:{
    now_user(){
      return this.$store.getters.register_user
    }
  },
  created(){
    console.log("数据获取。。。。。。。。。")
    this.getRequest(modelApi).then(res => {
      if (res) {
        this.texts_audio = res.texts_audio
        this.texts_video = res.texts_video
        console.log("数据获取完成....打印数据")
        this.user=this.$store.getters.register_user
        console.log("打印this.user")
        console.log(this.user)
        console.log("数据获取完成....打印数据")
        console.log(this.texts_audio)
        console.log(this.texts_video)

        this.dataReady = true; // 数据准备完毕

        // const nameArray = this.questionnaires.map(item => item.id);
        // this.tab_list=nameArray
        // console.log(this.tab_list)
      }
    })
    //
    // this.texts_audio = jsondata.texts_audio
    // this.texts_video = jsondata.texts_video
    // this.user=this.$store.getters.register_user
    // console.log("打印this.user")
    // console.log(this.user)
    // console.log("数据获取完成....打印数据")
    // console.log(this.texts_audio)
    // console.log(this.texts_video)
    // const nameArray = this.questionnaires.map(item => item.id);
    // this.tab_list=nameArray
    // console.log(this.tab_list)
  },
  components: {
    'Questionnaire' : questionnaire,
    'Audio' : Audio,
    'Audio2' : Audio2,
    'Video' : Video,
    User_contact : user_contact
  }
}
</script>
<style scoped>
.content {
  width: 75%;
}
</style>
