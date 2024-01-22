<template>
  <div class="content">
    <el-tabs ref="myTabs" v-model="activeName" @tabComplete="switchToTab">
      <el-tab-pane label="用户协议" name="first" style="width: 100%">
          <User_contact  @go-to-next-tab="goToNextTab"></User_contact>
      </el-tab-pane>
      <el-tab-pane
        :label="questionnaire.questionnaire_name"
        :name="'tab_' + questionnaire.id"
        v-for="questionnaire in questionnaires"
        :key="questionnaire.id"
      >
        <Questionnaire
          @go-to-next-tab="goToNextTab"
          @go_to_next_menu="completeNextModel"
          :questionnaire="questionnaire"
          :user="now_user"
          :tablist="tab_list"></Questionnaire>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
// 题目接口
import { getRequest } from '@/api/baseapi'
import jsondata from '../../../static/API.json'
import questionnaire from '@/views/front_myself/information/component/Questionnaire'
import user_contact from '@/views/front_myself/information/user_contact'
const modelApi = '/front/get_all2'
export default {
  name: 'qurs',
  data() {
    return {
      activeName: 'first',
      questionnaires: [],
      tab_list: [],
      user: null
    }
  },
  computed:{
    now_user(){
      return this.$store.getters.register_user
    }
  },
  methods: {
    completeNextModel() {
      this.$emit("go_to_next_menu")
    },
    goToNextTab() {
      console.log(this.activeName)
      let currentIndex='first'
      if (this.activeName!=='first') {
        currentIndex = this.questionnaires.findIndex(
          (questionnaire) => questionnaire.id === parseInt(this.activeName.split('_')[1])
        );
      }else {
        this.activeName = `tab_${this.questionnaires[0].id}`
      }
      console.log("currentIndex::",currentIndex)
      if (currentIndex !== -1 && currentIndex < this.questionnaires.length - 1) {
        this.activeName = `tab_${this.questionnaires[currentIndex + 1].id}`;
      }
      },
    switchToTab(tabName) {
      console.log('tabName:',tabName)
      this.activeName = tabName;
    },
    init_data(){
      this.getRequest(modelApi).then(res => {
        if (res) {
          this.questionnaires = res.questionnaires
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
  // beforeCreate() {
  created() {
    this.getRequest(modelApi).then(res => {
      if (res) {
        this.questionnaires = res.questionnaires
        console.log("数据获取完成....打印数据")
        console.log(this.questionnaires)
        const nameArray = this.questionnaires.map(item => item.id);
        this.tab_list=nameArray
        console.log(this.tab_list)
      }
    })
    // this.questionnaires = jsondata.questionnaires
    // console.log("数据获取完成....打印数据")
    // console.log(this.questionnaires)
    // const nameArray = this.questionnaires.map(item => item.id);
    // this.tab_list=nameArray
    // console.log("tablist::",this.tab_list)


  },
  mounted() {
    this.user=this.$store.getters.register_user
    console.log("打印this.user")
    console.log(this.user)
    const tabList = this.$refs.myTabs.$children.map(child => ({
      // label: child.label,
      name: child.name
    }));
    console.log("tabList222::",tabList)
  },
  updated() {

  },
  components: {
    'Questionnaire' : questionnaire,
    'User_contact' : user_contact
  }
}
</script>
<style scoped>
.content {
  width: 75%;
}
</style>
