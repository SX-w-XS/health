<template>
  <div>
    <el-questionnaire
      ref="mychild"
      :objSource="displayObj"
      :dataSource="dataSource"
      :load="loading"
      :item="item"
      :isDisabled="isDisabled"
      :isPlaceholder="isPlaceholder"
      btnText="提交"
    />
  </div>
</template>
<script>
import ElQuestionnaire from '@/components/survey_mobile_component/Questionnaire'
export default {
  name: 'survey_mobile',
  data(){
    return {
      item:{name:"问卷调查",status:"edit"},
      isDisabled:false,
      loading:false,
      isPlaceholder:"",
      dataSource: [
        {
          title: '一、基本情况',
          shortOption: [
            {label: "姓名", paramStr: "name", placeholder: "请输入姓名", value: "", errorMsg: "请输入姓名"},
            {label: '电话', paramStr: "mobile", placeholder: "请输入电话", value: "", errorMsg: "请输入电话"}
          ],
          isChildAnswer: "1",
          value: "1",
        },
        {
          title: '二、工作情况', shortOption: [],
          choiceOption: [
            {
              value: [],
              paramStr: "gradate",
              title: "工作几年？",
              type:"checkbox",
              list: ['1年-3年', "3年-5年", "5年以上"],
              errorMsg: "请选择工作年限，如果选择了其他,请填写"
            },
            {
              value: "",
              paramStr: "job",
              isOther: true,
              title: "从事什么职业",
              otherValue: "",
              list: ['前端开发', "后端开发", "测试", "产品经理"],
              errorMsg: "请选择所从事的职业"
            },
          ],
          isChildAnswer: "1",
          value: "1",
        },
        {
          title: '三、其他情况', shortOption: [],
          choiceOption: [
            {
              value: "",
              paramStr: "fruit",
              title: "是否喜欢吃水果",
              otherValue: "",
              isChildAnswer: "是",
              list: ['是', '否'],
              errorMsg: "请选择是否喜欢吃水果",
              shortOption: [
                {label: "最喜欢的水果种类", paramStr: "fruit_kind", placeholder: "请输入最喜欢的水果种类", value: "", errorMsg: "请输入最喜欢的水果种类"}
              ],
              choiceOption: [{
                value: "",
                paramStr: "fruit_link",
                title: "喜欢吃的水果",
                otherValue: "",
                list: ['苹果', '香蕉', '梨子'],
                errorMsg: "请选择喜欢吃的水果"
              }],
            },
            {
              value: [],
              type:"checkbox",
              paramStr: "sport",
              title: "喜欢什么运动",
              isOther: true,
              otherValue: "",
              list: ['篮球', '足球', '羽毛球'],
              errorMsg: "请选择喜欢的运动"
            },
          ],
          isChildAnswer: "1",
          value: "1",
        }
      ],
      displayObj:{},
    }
  },
  methods:{

  },
  components:{
    'el-questionnaire': ElQuestionnaire
  }
}
</script>
<style scoped>

</style>
