<template>
  <div>
    <el-form-item class="cm-bottom  sel-mar-10 cm-fw-bold">
      <div><span v-if="items.errorMsg" class="cm-c-red">* </span>{{ items.title }}</div>
      <el-radio-group v-if="items.type != 'checkbox'" v-model="items.value" class="cm-width-full">
        <el-radio v-for="(item,index) in items.list" :key="index" :label="item" :disabled="disabled" class="sel-width-35" />
        <div v-if="items.isOther" class="cm-mb-10 cm-flex cm-ai-c">
          <el-radio label="其他" class="sel-width-35" :disabled="disabled" />
          <input v-if="items.value == '其他'" v-model="items.otherValue" class="sel-input" :disabled="disabled" placeholder="请输入">
        </div>
        <el-alert
          v-if="(items.value == ''||items.value == '其他' && !items.otherValue) && isShow && items.errorMsg"
          :title="items.errorMsg"
          type="error"
          show-icon
          effect="light"
        />
      </el-radio-group>
      <el-checkbox-group v-if="items.type == 'checkbox'" v-model="items.value" class="cm-width-full sel-line-height">
        <el-checkbox v-for="(item,index) in items.list" :key="index" name="type" :disabled="disabled" :label="item" class="sel-width-35" />
        <div v-if="items.isOther" class="cm-mb-10 cm-flex cm-ai-c">
          <el-checkbox label="其他" :disabled="disabled" class="sel-width-35 sel-checkbox-mr" />
          <input v-if="items.value &&(items.value != null) && items.value.indexOf('其他')>-1" v-model="items.otherValue" class="sel-input" maxlength="20" :disabled="disabled" placeholder="请输入">
        </div>
        <el-alert
          v-if="(items.value && items.value.length == 0||(items.value.indexOf('其他')>-1 && !items.otherValue)) && isShow && items.errorMsg"
          :title="items.errorMsg"
          type="error"
          show-icon
          effect="light"
        />
      </el-checkbox-group>
    </el-form-item>
    <slot v-if="items.value == items.isChildAnswer" />
  </div>
</template>
<script>
import '../index.css'
let self
export default {
  name: 'Select',
  props: {
    items: {
      type: Object,
      default: {}
    },
    isShow: {
      type: Boolean,
      default: false
    }, disabled: {
      default: false
    }, type: {
      type: String,
      default: ''
    }
  },
  data() {
    return {

    }
  },
  created() {
    self = this
  },
  methods: {}
}
</script>
<style>
.sel-width-35{
  width: 40%;
  line-height: 40px;
}
.sel-checkbox-mr{
  margin-right: 30px!important;
}
.sel-mar-10{
  padding:0 1rem;
  margin-bottom: 0;
}
.sel-input{
  -webkit-appearance: none;
  border-radius: 4px;
  border: 1px solid #DCDFE6;
  box-sizing: border-box;
  color: #606266;
  font-weight: 500;
  font-size: 0.875rem;
  opacity:1;
  outline: 0;
  height: 2rem;
  padding: 0 0.3rem;
  width: 150px;
}
input:disabled,input[disabled]{
  color: #606266;
  font-weight: 500;
  opacity:1
}
textarea:disabled,textarea[disabled]{
  color: #606266;
  font-weight: 500;
  opacity:1
}
.sel-line-height{
  line-height: 1;
}
.el-checkbox__input.is-disabled+span.el-checkbox__label{
  color: #606266!important;
  opacity:1
}
.el-radio__input.is-disabled+span.el-radio__label{
  color: #606266!important;
  opacity:1
}
</style>
