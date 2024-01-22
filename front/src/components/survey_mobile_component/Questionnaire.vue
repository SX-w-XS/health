<template>
  <div
    v-loading="load"
    v-loading.fullscreen.lock="load"
    element-loading-text="提交中,请稍候..."
    element-loading-spinner="el-icon-loading"
  >
    <div class="cm-flex cm-jc-c cm-ptb-08">
      <div class="cm-fw-bold cm-pr-10 cm-fs-12">{{ item.name }}</div>
    </div>
    <el-form>
      <div v-for="itemOption in dataSource">
        <div class="cm-bottom cm-pad-08-10 cm-fw-bold cm-fs-11">{{ itemOption.title }}</div>
        <el-list
          v-for="(item,index) in itemOption.shortOption"
          :key="item.label"
          class="fs-0875"
          :is-placeholder="isPlaceholder"
          :item="item"
          :disabled="isDisabled"
          :is-show="isShow"
        />
        <el-select v-for="(list,index) in itemOption.choiceOption" :key="index" :items="list" :disabled="isDisabled" :is-show="isShow">
          <div class="expand-style">
            <el-list
              v-for="(item,index) in list.shortOption"
              :key="item.label"
              :item="item"
              :disabled="isDisabled"
              :is-placeholder="isPlaceholder"
              :is-show="isShow"
            />
            <el-select
              v-for="(list,index) in list.choiceOption"
              :key="index"
              :items="list"
              :disabled="isDisabled"
              :is-placeholder="isPlaceholder"
              :is-show="isShow"
            />
          </div>
        </el-select>
      </div>
      <el-form-item class="cm-fw-bold">
        <label class="cm-ml-10">其他建议 </label>
        <div class="cm-flex flex-fill">
          <textarea
            id=""
            ref="textarea"
            v-model="other_advice"
            maxlength="500"
            name=""
            :placeholder="isPlaceholder!='无'?'请输入您的建议':isPlaceholder"
            class="hos-textarea"
            :disabled="isDisabled"
          />
        </div>
      </el-form-item>
      <div v-if="item.status==='edit'" class="hos-btn" @click="submitForm()">{{ btnText }}</div>
    </el-form>
  </div>
</template>
<script>
import '../index.css'
import select from './Select.vue'
import list from './List.vue'
let self
export default {
  name: 'ElQuestionnaire',
  components: {
    'el-select': select,
    'el-list': list
  },
  props: {
    dataSource: {
      type: Array,
      default: []
    },
    objSource: {
      type: Object,
      default: {}
    },
    load: {
      type: Boolean,
      default: true
    },
    item: {
      type: Object,
      default: {}
    },
    isDisabled: {
      // eslint-disable-next-line vue/require-prop-type-constructor
      type: String | Boolean,
      default: false
    },
    isPlaceholder: {
      type: String,
      default: ''
    },
    btnText: {
      type: String,
      default: '提交'
    }
  },
  data() {
    return {
      other_advice: '',
      isShow: false
    }
  },
  created() {
    self = this
  },
  mounted() {
    var textarea = document.getElementsByTagName('textarea')
    // 多行输入框高度自适应
    setTimeout(function() {
      for (var i = 0; i < textarea.length; i++) {
        textarea[i].style.height = textarea[i].scrollHeight + 'px'
        textarea[i].addEventListener('input', function(e) {
          e.target.style.height = 'auto'
          e.target.scrollTop = 0 // 防抖动
          e.target.style.height = e.target.scrollHeight + 'px'
        })
      }
    }, 200)
  },
  methods: {
    // 提交
    submitForm() {
      self.isShow = true
      var arr = []
      var obj = {}
      self.generate(self.dataSource, {}, arr, obj)
      obj = Object.assign(obj, { 'other_advice': self.other_advice })
      console.log(obj)
      this.$parent.submit(arr, obj)
    },
    // 将数据源轮循
    generate: (list, displayObj, arr, obj) => {
      list.map((item) => {
        if (arr && obj) {
          if (item && item.value !== undefined && item && item.paramStr !== undefined) {
            // 多选如果有其他，将其他数值添加进去
            let value
            // 其他值不等于空并且不是填空
            // eslint-disable-next-line eqeqeq
            if (item.otherValue != '' && item.otherValue != undefined && !item.label) {
              if (item.type === 'checkbox') {
                if (!item.value.includes(item.otherValue)) {
                  item.value.push(item.otherValue)
                }
                // 有其他值反选值，但是其他label没有勾选，就将其他值去掉
                if (item.value.includes(item.otherValue) && !item.value.includes('其他')) {
                  // eslint-disable-next-line eqeqeq
                  item.value = item.value.filter((item1) => { return item1 != item.otherValue })
                }
                value = item.value
              } else {
                if (item.otherValue && item.value === '其他') {
                  value = item.otherValue
                }
              }
            } else {
              console.log(item)
              value = item.value
              // 如果其他值为空，但是选择了“其他”，则需要校验
              if (item.value.indexOf('其他') > -1 || item.value === '其他') {
                arr.push({ 'value': item.otherValue })
              }
            }
            obj = Object.assign(obj, { [item.paramStr]: value })
            if (item.errorMsg) {
              arr.push({ 'value': item.value })
            }
          }
          if (item.isChildAnswer && item.value === item.isChildAnswer) {
            if (item.shortOption && item.shortOption.length > 0) {
              self.generate(item.shortOption, {}, arr, obj)
            }
            if (item.choiceOption && item.choiceOption.length > 0) {
              self.generate(item.choiceOption, {}, arr, obj)
            }
          }
        } else {
          if (item && item.value !== undefined && item && item.paramStr !== undefined) {
            if (displayObj[item.paramStr]) {
              if (item.type === 'checkbox' && displayObj[item.paramStr] && displayObj[item.paramStr].length > 0) {
                item.value = displayObj[item.paramStr]
                const allList = item.list.concat(displayObj[item.paramStr])
                item.value.map((res) => {
                  if (item.list.indexOf(res) < 0) {
                    item.isOther = true
                    if (item.otherValue != res) {
                      item.otherValue = res
                    }
                  }
                })
                // value去重
                item.value = item.value.filter((item1, index) => {
                  return item.value && item1 && item.value.indexOf(item1) === index
                })
                // 如果返回的值中有与页面值不同的则添加到页面值中
                item.list = allList.filter((item1, index) => {
                  return (allList.indexOf(item1)) === index && item1 && item1 != item.otherValue && item1 != '其他'
                })
              } else if (item.list && item.type != 'checkbox') {
                if (item.list.indexOf(displayObj[item.paramStr]) < 0 && displayObj[item.paramStr]) {
                  item.isOther = true
                  item.value = '其他'
                  item.otherValue = displayObj[item.paramStr]
                } else {
                  item.value = displayObj[item.paramStr]
                }
              } else {
                item.value = displayObj[item.paramStr]
              }
            }
          }
          if (item.isChildAnswer && item.value === item.isChildAnswer) {
            if (item.shortOption && item.shortOption.length > 0) {
              self.generate(item.shortOption, displayObj)
            }
            if (item.choiceOption && item.choiceOption.length > 0) {
              self.generate(item.choiceOption, displayObj)
            }
          }
          if (displayObj.other_advice) {
            self.other_advice = displayObj.other_advice
          }
        }
      })
      return { obj, arr }
    }
  }
}
</script>

<style>
.expand-style {
  font-size: 0.875rem;
  /*background: #f5f5f5;*/
}
.fs-0875{
  font-size: 0.875rem;
}
.hos-btn {
  background: #409EFF;
  color: #fff;
  margin: 1rem;
  padding: 0.8rem 0;
  text-align: center;
  border-radius: 0.5rem;
}

.hos-textarea {
  margin: 0 1rem;
  word-break: break-all;
  resize: none;
  border-radius: 0.3rem;
  outline: none;
  line-height: 1rem;
  width: 100%;
  border: 1px solid #ddd;
  font-size: 0.8rem;
  color: #333;
  padding:0.5rem;
}

</style>
