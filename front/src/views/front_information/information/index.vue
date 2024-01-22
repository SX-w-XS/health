<template>
  <div class="allInformation">
    <div class="title">xxxxx管理系统</div>
    <el-tabs type="border-card">
      <el-tab-pane label="信息录入">
        <person-information></person-information>
      </el-tab-pane>
      <el-tab-pane label="心理测评">
        <psychologyTest
          :questionnaires="studyData.questionnaires"
        ></psychologyTest>
      </el-tab-pane>
      <el-tab-pane label="声音录制">
        <voice :audioData="studyData.texts_audio"></voice>
      </el-tab-pane>
      <el-tab-pane label="视频朗读">
        <Camera :videoData="studyData.texts_video"></Camera>
      </el-tab-pane>
      <el-tab-pane label="信息回答">信息回答</el-tab-pane>
      <el-tab-pane label="其他">其他</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Camera from './camera.vue'
import psychologyTest from './psychologyTest.vue'
import voice from './voice.vue'
import personInformation from './personInformation.vue'
import jsondata from '../../../static/API.json'

export default {
  name: 'PbcodeIndex',

  data() {
    return {
      studyData: {}
    }
  },

  components: {
    personInformation,
    Camera,
    psychologyTest,
    voice
  },

  mounted() {
    this.getData()
  },

  methods: {
    getData() {
      // let data = jsondata
      this.studyData = jsondata
      // jsondata
      // this.getRequest("/static/API.json").then((res) => {
      //   //请求本地文件必须放在public中 本地/static/API.json  远程/front/get_all
      //   let data = res.data;
      //   this.studyData = data;
      // });
    }
  }
}
</script>

<style lang="scss" scoped>
.title {
  font-size: 20px;
  font-weight: bold;
  margin: 10px 0;
}

.allInformation {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
}
</style>
