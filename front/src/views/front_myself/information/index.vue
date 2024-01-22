<template>
  <div class="">
    <el-container class="container">
      <el-header class="title">青少年心理情绪识别</el-header>
      <el-main class="container">
        <div class="nav_menus">
          <el-menu
            :default-active="activeTab"
            class="el-menu-demo"
            mode="horizontal"
          >
            <el-menu-item
              v-for="tab in tablist"
              :index="tab.index_order"
              :name="tab.name"
              :label="tab.label"
              :route="tab.name"
              :key="tab.index_order"

              @click="tabClick(tab)"
            >
              <!--              :disabled="userId <= 0 && tab.name != 'Register_user'"-->
              <div> {{ tab.label }}</div>
            </el-menu-item>
          </el-menu>
          <div class="line"></div>
        </div>
        <keep-alive>
          <router-view      @go_to_next_menu="next_menux"></router-view>
        </keep-alive>

      </el-main>
<!--      <el-footer>Footer</el-footer>-->
    </el-container>
  </div>
</template>

<script>
import jsondata from '../../../static/API.json'

export default {
  name: 'Index_myself',

  data() {
    return {
      activeTab: '1',
      activeTabidx:0,
      tablist: [
        {
          label: '信息录入',
          index_order: '1',
          name: 'Register_user',
          content: 'Tab 1 content'
        },
        {
          label: '问卷录入',
          index_order: '2',
          name: 'questionnaire',
          content: 'Tab 2 content',
        },
        {
          label: '朗读文本',
          index_order: '3',
          name: 'read_text',
          content: 'audio_langdu_page'
        },
        {
          label: '问题回答',
          index_order: '4',
          name: 'interview'
        },
        {
          label: '其他',
          index_order: '5',
          name: 'other_page',
          content: 'other'
        }
      ]
    }
  },
  computed: {
    userId() {
      let userId = this.$store.state.front_user.register_user.id
      return userId ? userId : 0
    }
  },
  components: {},

  mounted() {
    this.getData()
    console.log(this.$route.fullPath)
    // 当前path
    let path=this.$route.fullPath
    // 提取 /front_myself/ 后面以 / 或 ? 结尾的字符
    const regex = /\/front_myself\/([^/?]+)/;
    const match = path.match(regex);
    let result = match[1];
    console.log("match",match)
    this.activeTabidx=this.tablist.findIndex(item => item.name === result);
    this.activeTab=this.tablist[this.activeTabidx].index_order
    // this.$router.push({path:})
  },

  methods: {
    //tab点击
    tabClick(targetName) {
      this.activeTab=targetName.index_order
      this.activeTabidx=this.tablist.findIndex(item => item.name === targetName.name);
      console.log('this.activeTab',this.activeTab)
      this.$router.push({ path: '/front_myself/' + targetName.name })
    },
    next_menux(){
      console.log("进入导航冒泡.......")
      console.log("当前idx:",this.activeTabidx)
      console.log("当前长度:",this.tablist.length)
      if (this.activeTabidx>=this.tablist.length-1)this.activeTabidx=-1
      let targetName=this.tablist[++this.activeTabidx]
      this.tabClick(targetName)
    },
    getData() {
      return ''
      /*       let data = jsondata
            this.studyData = jsondata */
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

.container {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
  align-content: center;
  align-items: center;
}

.title {
  font-size: 40px;
  font-weight: bold;
  margin: 20px 0  -34px;
}

.nav_menus {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
}

</style>
