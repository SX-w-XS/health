<template>
  <div
    :class="disabled == 'disabled'?'list-bg-disabled':(item.value==''?'':'list-bg')"
  >
    <div class="cm-plr-10 cm-bottom">
      <div v-if="!item.isArea" class="cm-flex cm-fw-bold cm-ai-c">
        <label for=""><span v-if="item.errorMsg" class="cm-c-red"> * </span>
          {{ item.label }}
        </label>
        <input
          v-model="item.value"
          :placeholder="isPlaceholder!='无'?item.placeholder:isPlaceholder"
          class="list-input"
          :disabled="disabled"
        >
      </div>
      <div v-if="item.isArea" class="cm-fw-bold">
        <div class="cm-pt-10"><span v-if="item.errorMsg" class="cm-c-red"> * </span>{{ item.label }}</div>
        <textarea
          v-model="item.value"
          maxlength="500"
          :placeholder="isPlaceholder!='无'?item.placeholder:isPlaceholder"
          :class="disabled == 'disabled'?'list-textarea-disabled':(item.value!=''?'list-textarea-value':'list-textarea')"
          :disabled="disabled"
        />
      </div>
      <el-alert
        v-if="item.value == ''&& isShow && item.errorMsg"
        :title="item.errorMsg"
        type="error"
        show-icon
        effect="light"
      />
    </div>
  </div>
</template>
<script>
import '../index.css'
export default {
  name: 'List',
  props: {
    item: {
      type: Object,
      default: {}
    },
    isShow: {
      type: Boolean,
      default: false
    }, disabled: {
      default: false
    }, isPlaceholder: {
      type: String,
      default: ''
    }
  },
  data() {
    return {

    }
  },
  created() {},
  methods: {}
}
</script>
<style scoped>
.list-input{
  height: 3rem;
  text-align: right;
  flex: 1;
  font-size: 0.875rem;
  color: #000;
  opacity:1
}
input:disabled,input[disabled]{
  color: #000;
  opacity:1
}
textarea:disabled,textarea[disabled]{
  color: #000;
  opacity:1
}
.list-textarea{
  font-size: 0.875rem;
  color: #333;
  width: 100%;
  border: none;
  margin: 0.5rem 0;
  background: #fff;
  outline: none;
}
.list-textarea-value{
  font-size: 0.875rem;
  color: #333;
  width: 100%;
  border: none;
  margin: 0.5rem 0;
  background: #f5f5f9;
  outline: none;
}
.list-textarea-disabled{
  background-color: #f5f5f5;
  font-size: 0.875rem;
  color: #333;
  width: 100%;
  border: none;
  margin: 0.5rem 0;
  outline: none;
}
.list-bg{
  background: #f5f5f5;
}
.list-bg-disabled{
  background-color: #f5f5f5;
}
input::-webkit-input-placeholder,textarea::-webkit-input-placeholder{
  font-size: 0.875rem;
}
</style>
