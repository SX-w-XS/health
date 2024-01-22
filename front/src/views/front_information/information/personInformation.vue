<template>
  <div class="peronInformation">
    <el-form
      label-position="left"
      label-width="80px"
      :model="personInformation"
    >
      <el-form-item label="姓名">
        <el-input v-model="personInformation.name"></el-input>
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="personInformation.sex">
          <el-option value="1" label="男"></el-option>
          <el-option value="0" label="女"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="年龄">
        <el-input v-model="personInformation.age"></el-input>
      </el-form-item>
      <el-form-item label="职业">
        <el-input v-model="personInformation.career"></el-input>
      </el-form-item>
      <el-form-item label="是否在读">
        <el-select v-model="personInformation.isRead">
          <el-option value="true" label="是"></el-option>
          <el-option value="false" label="否"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="最高学历">
        <el-input v-model="personInformation.maxRead"></el-input>
      </el-form-item>
      <el-form-item label="家庭信息">
        <el-input v-model="personInformation.family"></el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "PbcodePersonInformation",

  data() {
    return {
      personInformation: {
        name: "",
        sex: "1",
        age: "",
        career: "",
        isRead: "false",
        maxRead: "",
        family: "",
      },
    };
  },

  mounted() {},

  methods: {},
};
</script>

<style lang="scss" scoped>
</style>