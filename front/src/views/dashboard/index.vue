<template>
  <div class="dashboard-container">
    欢迎使用基于机器学习的情绪诊断系统
    <div class="dashboard-text">Hi, {{ name }}</div>
    <br>
    <div><h2>{{ tipMessage }}</h2></div>
    dashbord显示 直接诊断页面，
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      tipMessage: '早上好,来杯☕吧～今天工作也要加油鸭！奥利给！！！🏆'
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  created() {
    const currentHour = (new Date()).getHours()
    if ((currentHour >= 0 && currentHour <= 6) || (currentHour >= 22 && currentHour <= 24)) {
      this.tipMessage = '夜深了,早点下班~明天继续加油😘'
    } else if (currentHour >= 11 && currentHour < 13) {
      this.tipMessage = '中午好,午饭吃什么想好了吗?🤣'
    } else if (currentHour >= 13 && currentHour <= 16) {
      this.tipMessage = '下午好,早上效率如何?今天的计划能完成吗😃'
    } else if (currentHour >= 17 && currentHour <= 18) {
      this.tipMessage = '傍晚好,今天是按时下班还是加班呢🤪'
    } else if (currentHour >= 19 && currentHour <= 21) {
      this.tipMessage = '晚上好,加班辛苦啦~加油🤞'
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
