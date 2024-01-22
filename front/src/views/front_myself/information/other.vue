<template>
  <div>
<!--      <zujian         @go_to_next_menu="completeNextModel"></el-button>-->
      <el-button           @click="completeNextModel">我是btn</el-button>
  </div>
</template>
<script>
export default {
  name: 'other',
  data() {
    return {}
  },
  methods: {
    completeNextModel() {
      this.$emit("go_to_next_menu")
    },
  },
  components: {}
}
</script>
<style scoped>

</style>
